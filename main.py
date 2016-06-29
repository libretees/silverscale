#!/usr/bin/env python
# -*- coding: utf-8 -*-

from silverscale.device import ScaleManager

device_manager = ScaleManager()

for device in device_manager.devices:
    device.connect()
    print(device.manufacturer, device.product, device.serial_number)

    for i in range(3):
        report = device.read()
        print(report)

device_manager.close()

