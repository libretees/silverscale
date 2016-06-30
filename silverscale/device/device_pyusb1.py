#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import usb.core
import usb.util
from ..usb_ids import SUPPORTED_DEVICES


class USBDevice(object):
    def __init__(self, device):
        self._device = device
        self._reattach = False

    @property
    def manager(self):
        return self._manager()

    @property
    def product(self):
        return usb.util.get_string(self._device, self._device.iProduct)

    @property
    def manufacturer(self):
        return usb.util.get_string(self._device, self._device.iManufacturer)

    @property
    def serial_number(self):
        return usb.util.get_string(self._device, self._device.iSerialNumber)

    def connect(self):
        for configuraton in self._device:
            for interface in configuraton:
                interface_number = interface.bInterfaceNumber
                if self._device.is_kernel_driver_active(interface_number):
                    try:
                        self._device.detach_kernel_driver(interface_number)
                    except usb.core.USBError as e:
                        sys.exit(
                            'Could not detach kernel driver from interface(%s): %s' %
                            (interface_number, str(e)))
                    else:
                        self._reattach = True

        # use the first/default configuration
        self._device.set_configuration()
        configuration = self._device.get_active_configuration()

        # Match the first IN endpoint.
        interface = configuraton[(0,0)]
        self._endpoint_in = usb.util.find_descriptor(
            interface,
            custom_match = \
            lambda e: \
                usb.util.endpoint_direction(e.bEndpointAddress) == \
                usb.util.ENDPOINT_IN)

        self._endpoint_out = usb.util.find_descriptor(
            interface,
            custom_match = \
            lambda e: \
                usb.util.endpoint_direction(e.bEndpointAddress) == \
                usb.util.ENDPOINT_OUT)

        if self not in self.manager:
            self.manager.add(self)

    def disconnect(self):
        self._device.reset()
        usb.util.dispose_resources(self._device)

        if self._reattach:
            self._device.attach_kernel_driver(0)

        self.manager.remove(self)

    def read(self, packet_size=None):
        if packet_size is None:
            packet_size = self._endpoint_in.wMaxPacketSize

        report = None
        while report is None:
            try:
                report = self._device.read(self._endpoint_in.bEndpointAddress,
                                           packet_size)
            except usb.core.USBError as e:
                report = None

        return list(report)

    def write(self, packet):
        result = None
        if self._endpoint_out is not None:
            result = self._endpoint_out.write(packet)

        return result == len(packet)


class _USBDeviceManager(object):

    device_class = USBDevice

    def __init__(self):
        devices = usb.core.find(find_all=True,
                                custom_match=
                                    lambda x: (x.idVendor, x.idProduct) in SUPPORTED_DEVICES)
        self._devices = [self.device_class(device) for device in devices]

    def __call__(self, *args, **kwargs):
        return self

    def __contains__(self, item):
        return item in self._devices

    @property
    def devices(self):
        return self._devices

    def add(self, x):
        self._devices.append(x)

    def remove(self, x):
        if x in self._devices:
            self._devices.remove(x)

    def close(self):
        for device in self._devices:
            device.disconnect()

