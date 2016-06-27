#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import time
from silverscale.device.device_cython_hidapi import USBDeviceManager
from silverscale.reports import REPORT_TYPES

device_manager = USBDeviceManager()

for device in device_manager.devices:
    print(device.manufacturer, device.product, device.serial_number)

    for k in range(10):
        report_data = device.read(6)
        if report_data:
            report = REPORT_TYPES[report_data[0]](report_data)
            print(report)

        time.sleep(0.05)

device_manager.close()
print('Done')
