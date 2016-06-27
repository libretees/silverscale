#!/usr/bin/env python
# -*- coding: utf-8 -*-

from silverscale.device.device_libusb1 import USBDeviceManager

device_manager = USBDeviceManager()

for device in device_manager.devices:
    print(device.manufacturer, device.product)
    device.connect()
    data = device.read(6)
    print(data)

device_manager.close()

print('Exit')

