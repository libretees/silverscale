#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import usb1
from libusb1 import USB_ENDPOINT_DIR_MASK
from ..usb_ids import SUPPORTED_DEVICES

class USBDevice(object):
    def __init__(self, device):
        self._device = device
        self._device_handle = None
        self._interface = None
        self._reattach = False

    @property
    def manager(self):
        return self._manager()

    @property
    def product(self):
        return self._device.getProduct()

    @property
    def manufacturer(self):
        return self._device.getManufacturer()

    @property
    def serial_number(self):
        return self._device.getSerialNumber()

    def connect(self):
        self._device_handle = self._device.open()

        for configuraton in self._device_handle.getDevice():
            for interface in configuraton:
                for interface_setting in interface:
                    if self._device_handle.kernelDriverActive(interface_setting.getNumber()):
                        try:
                            self._device_handle.detachKernelDriver(interface_setting.getNumber())
                        except usb1.USBErrorIO as e:
                            sys.exit(
                                'Could not detach kernel driver from interface(%s): %s' %
                                (interface_setting, str(e)))
                        else:
                            self._interface = interface_setting
                            self._reattach = True

        endpoints = [
            endpoint
            for configuration in self._device
            for interface in configuration
            for interface_setting in interface
            for endpoint in interface_setting]

        self._endpoint_in, self._endpoint_out = None, None
        for endpoint in endpoints:
            endpoint_in = bool(USB_ENDPOINT_DIR_MASK & endpoint.getAddress())

            if endpoint_in and self._endpoint_in is None:
                self._endpoint_in = endpoint
            elif not endpoint_in and self._endpoint_out is None:
                self._endpoint_out = endpoint

        if self not in self.manager:
            self.manager.add(self)

    def disconnect(self):
        if self._device_handle is not None:
            if self._reattach:
                self._device_handle.attachKernelDriver(self._interface.getNumber())
            self._device_handle.close()

        self._device.close()

        self.manager.remove(self)

    def read(self, packet_size=None):
        if packet_size is None:
            packet_size = self._endpoint_in.getMaxPacketSize()

        try:
            report_data = self._device_handle.bulkRead(self._endpoint_in.getAddress(),
                                                       packet_size)
        except usb1.USBErrorIO as e:
            sys.exit(str(e))

        if sys.version_info[0] < 3:
            report_data = map(ord, report_data)

        return list(report_data)

    def write(self, packet):
        result = None
        if self._endpoint_out is not None:
            result = self._device_handle.bulkWrite(self._endpoint_out.getAddress(),
                                                   packet)
        return result == len(packet)


class _USBDeviceManager(object):

    device_class = USBDevice

    def __init__(self):
        context = usb1.USBContext()
        devices = [
            device for device in context.getDeviceList(skip_on_error=True)
            if (device.getVendorID(), device.getProductID()) in SUPPORTED_DEVICES]
        self._devices = [self.device_class(device) for device in devices]

    def __call__(self, *args, **kwargs):
        return self

    def __contains__(self, item):
        return item in self._devices

    @property
    def devices(self):
        return self._devices

    def add(self, x):
        if x not in self._devices:
            self._devices.append(x)

    def remove(self, x):
        if x in self._devices:
            self._devices.remove(x)

    def close(self):
        for device in self._devices:
            device.disconnect()

