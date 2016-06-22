#!/usr/bin/env python
# -*- coding: utf-8 -*-

import hid
import time
from silverscale.reports import REPORT_TYPES
from silverscale.usb_ids import SUPPORTED_DEVICES

connected_devices = [
    (device_info.get('vendor_id'), device_info.get('product_id'))
    for device_info in hid.enumerate()
]

connected_scales = [
    device for device in connected_devices if device in SUPPORTED_DEVICES
]

class Scale(hid.device):
    def __init__(self, *args, **kwargs):
        super(Scale, self).__init__(*args, **kwargs)
        self._vendor_id, self._product_id = args

        self._open_device()

    def _open_device(self):
        self.open(vendor_id, product_id) # idVendor idProduct

scales = []
for vendor_id, product_id in connected_scales:
   try:
       scale = Scale(vendor_id, product_id) # idVendor idProduct
   except IOError as e:
       print(e)
   else:
       print('Manufacturer: %s' % scale.get_manufacturer_string())
       print('Product: %s' % scale.get_product_string())
       print('Serial No: %s' % scale.get_serial_number_string())
       scales.append(scale)
       print(scales)

if not scales:
    print('No scales are connected!')

for scale in scales:


    # try non-blocking mode by uncommenting the next line
    #scale.set_nonblocking(1)

    # try writing some data to the device
    for k in range(10):
        for i in [0, 1]:
            for j in [0, 1]:
                res = scale.write([0x80, i, j])
                report_data = scale.read(6)
                if report_data:
                    report = REPORT_TYPES[report_data[0]](report_data)
                    print(report)

                time.sleep(0.05)

    print('Closing device')
    scale.close()

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
