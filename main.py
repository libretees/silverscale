#!/usr/bin/env python
# -*- coding: utf-8 -*-

from silverscale.device import USBDeviceManager
from silverscale.reports import REPORT_TYPES

device_manager = USBDeviceManager()

for device in device_manager.devices:
    device.connect()
    print(device.manufacturer, device.product, device.serial_number)

    for i in range(3):
        report_data = device.read(6)
        if report_data:
            report = REPORT_TYPES[report_data[0]](report_data)
            print(report)

device_manager.close()

