#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import usb.core
import usb.util
from silverscale.usb_ids import SUPPORTED_DEVICES


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

        report = self._device.read(self._endpoint_in.bEndpointAddress, packet_size)

        return list(report)

    def write(self, packet):
        result = None
        if self._endpoint_out is not None:
            result = self._endpoint_out.write(packet)

        return result == len(packet)


class _DeviceManager(object):

    def __init__(self):
        devices = usb.core.find(find_all=True,
                                custom_match=
                                    lambda x: (x.idVendor, x.idProduct) in SUPPORTED_DEVICES)
        self._devices = [USBDevice(device) for device in devices]

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


DeviceManager = _DeviceManager()
USBDevice._manager = DeviceManager

device_manager = DeviceManager()

for device in device_manager.devices:
    device.connect()
    print(device.manufacturer, device.product, device.serial_number)

    # read a data packet
    attempts = 10
    data = None
    while data is None and attempts > 0:
        try:
            data = device.read()
            print(data)
        except usb.core.USBError as e:
            data = None
            if e.args == ('Operation timed out',):
                attempts -= 1
                continue

device_manager.close()

