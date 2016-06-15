#!/usr/bin/env python
# -*- coding: utf-8 -*-

import hid
import time

WEIGHT_UNIT = {
    0x0: 'units',  # Unknown Unit
    0x1: 'mg',     # Milligram
    0x2: 'g',      # Gram
    0x3: 'kg',     # Kilogram
    0x4: 'ct',     # Carat
    0x5: 'taels',  # Taels
    0x6: 'gr',     # Grains
    0x7: 'dwt',    # Pennyweight
    0x8: 'tonnes', # Metric Tons
    0x9: 'tons',   # Avoir Ton
    0xA: 'ozt',    # Troy Ounce
    0xB: 'oz',     # Ounce
    0xC: 'lbs'     # Pound
}

SCALE_STATUS = {
    0x0: 'Unknown Status',
    0x1: 'Fault',
    0x2: 'Stable at Center of Zero',
    0x3: 'In Motion',
    0x4: 'Weight Stable',
    0x5: 'Under Zero',
    0x6: 'Over Weight Limit',
    0x7: 'Requires Calibration',
    0x8: 'Requires Re-zeroing',
    0x10: 'Zero Scale',
    0x11: 'Enforced Zero Return'
}


def twos_complement(val, bits=8):
    if (val & (1 << (bits - 1))): # If sign bit is set e.g., 8bit: 128-255
        val = val - (1 << bits)   # compute negative value
    return val


for device_info in hid.enumerate():
    vendor_id = device_info.get('vendor_id')
    product_id = device_info.get('product_id')

    if vendor_id and product_id:
        try:
            device = hid.device()
            device.open(vendor_id, product_id)
        except IOError as e:
            print(e)
        else:
            print('Manufacturer: %s' % device.get_manufacturer_string())
            print('Product: %s' % device.get_product_string())
            print('Serial No: %s' % device.get_serial_number_string())


try:
    print('Opening device')
    h = hid.device()

    h.open(0x922, 0x8004) # idVendor idProduct

    print('Manufacturer: %s' % h.get_manufacturer_string())
    print('Product: %s' % h.get_product_string())
    print('Serial No: %s' % h.get_serial_number_string())

    # try non-blocking mode by uncommenting the next line
    #h.set_nonblocking(1)

    # try writing some data to the device
    for k in range(10):
        for i in [0, 1]:
            for j in [0, 1]:
                res = h.write([0x80, i, j])
                report = h.read(6)
                if report:
                    (report_type, scale_status, unit, scaling, weight_lsb,
                    weight_msb) = tuple(report)

                    weight = (weight_msb << 8) | weight_lsb
                    weight = weight * pow(10, twos_complement(scaling))

                    print(report)
                    print('scale status:', SCALE_STATUS[scale_status])
                    print('weight:', weight)
                    print('unit:', WEIGHT_UNIT[unit])

                time.sleep(0.05)

    print('Closing device')
    h.close()

except IOError as ex:
    print(ex)
    print('You probably don\'t have the hard coded test hid. Update the hid.device line')
    print('in this script with one from the enumeration list output above and try again.')

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
