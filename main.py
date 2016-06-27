#!/usr/bin/env python
# -*- coding: utf-8 -*-

from silverscale.device import USBDeviceManager

device_manager = USBDeviceManager()

for device in device_manager.devices:
    device.connect()
    print(device.manufacturer, device.product, device.serial_number)

    for i in range(3):
        data = device.read(6)
        print(data)

device_manager.close()

