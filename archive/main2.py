#!/usr/bin/env python
# -*- coding: utf-8 -*-

import usb.core
from silverscale.device.device_pyusb1 import USBDeviceManager

device_manager = USBDeviceManager()

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

