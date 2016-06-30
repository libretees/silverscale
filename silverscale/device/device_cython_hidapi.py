#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import hid
from ..usb_ids import SUPPORTED_DEVICES


class USBDevice(object):
    def __init__(self, device):
        assert device is not None
        self._device = device

    @property
    def manager(self):
        return self._manager()

    @property
    def product(self):
        return self._device.get_product_string()

    @property
    def manufacturer(self):
        return self._device.get_manufacturer_string()

    @property
    def serial_number(self):
        return self._device.get_serial_number_string()

    def connect(self):
        if self not in self.manager:
            self.manager.add(self)

    def disconnect(self):
        self._device.close()
        self.manager.remove(self)

    def read(self, packet_size=8):

        packet_size = min(packet_size, 8)

        report = []
        while len(report) < packet_size:
            try:
                bytes_read = self._device.read(packet_size)
            except IOError as e:
                sys.exit(str(e))
            else:
                report += bytes_read

        return report[:packet_size]

    def write(self, packet):
        return self._device.write(packet) == len(packet)


class _USBDeviceManager(object):

    device_class = USBDevice

    def __init__(self):
        connected_devices = [
            device_info.get('path')
            for device_info in hid.enumerate()
            if (device_info.get('vendor_id'), device_info.get('product_id'))
            in SUPPORTED_DEVICES and device_info.get('path') is not None
        ]

        devices = []
        for path in connected_devices:
            try:
                device = hid.device()
                device.open_path(path)
            except IOError as e:
                sys.exit(str(e))
            else:
                devices.append(device)

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

