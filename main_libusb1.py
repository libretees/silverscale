#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import usb1
from silverscale.usb_ids import SUPPORTED_DEVICES

context = usb1.USBContext()

devices = context.getDeviceList(skip_on_error=True)

devices = [device for device in devices if (device.getVendorID(),
           device.getProductID()) in SUPPORTED_DEVICES]

print(devices)
