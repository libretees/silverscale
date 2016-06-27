#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import time
import hid
from silverscale.reports import REPORT_TYPES
from silverscale.usb_ids import SUPPORTED_DEVICES


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

        return report

    def write(self, packet):
        return self._device.write(packet) == len(packet)


class _DeviceManager(object):

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

print('Devices found:', device_manager.devices)

for device in device_manager.devices:
    print(device.manufacturer, device.product, device.serial_number)

    # try non-blocking mode by uncommenting the next line
    #scale.set_nonblocking(1)

    # try writing some data to the device
    for k in range(10):
        # for i in [0, 1]:
        #     for j in [0, 1]:
        #         res = scale.write([0x80, i, j])
        #        print(res, type(res))
        report_data = device.read(6)
        if report_data:
            report = REPORT_TYPES[report_data[0]](report_data)
            print(report)

        time.sleep(0.05)

device_manager.close()
print('Done')
# =======
# from importlib import import_module
#
# for module_name in ('device_libusb1', 'device_pyusb1', 'device_pyusb',
#                     'device_ctypes_hidapi', 'device_cython_hidapi'):
#     try:
#         print(module_name)
#         module = import_module('silverscale.' + module_name)
#         USBDevice = getattr(module, 'USBDevice')
#         break
#     except ImportError as error:
#         print(error)
# else:
#     raise ImportError('No USB library found')
#
# scale = USBDevice(0x922, 0x8004)
#
# >>>>>>> 4b9ee7e9acc514437e3047fd5a66b04d09da085a
