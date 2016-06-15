#!/usr/bin/env python
# -*- coding: utf-8 -*-

import hid
import time

UNIT = [
    'units',  # Unknown Unit
    'mg',     # Milligram
    'g',      # Gram
    'kg',     # Kilogram
    'cd',     # Carat
    'taels',  # Taels
    'gr',     # Grains
    'dwt',    # Pennyweight
    'tonnes', # Metric Tons
    'tons',   # Avoir Ton
    'ozt',    # Troy Ounce
    'oz',     # Ounce
    'lbs'     # Pound
]

SCALE_STATUS = [
    'Unknown Status',
    'Fault',
    'Stable at Center of Zero',
    'In Motion',
    'Weight Stable',
    'Under Zero',
    'Over Weight Limit',
    'Requires Calibration',
    'Requires Re-zeroing'
]

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
                # scale_attribute, scale_control, scale_data, scale_status,
                # scale_weight_limit, scale_statistics = h.read(6)
                data = h.read(6)
                if data:
                    (report, scale_status, unit, scaling, weight_low,
                    weight_high) = tuple(data)

                    weight = (weight_high << 8) | weight_low
                    weight = weight * pow(10, scaling)

                    print(data, scaling)
                    print('scale status:', SCALE_STATUS[scale_status])
                    print('weight:', weight)
                    print('unit:', UNIT[unit])

                time.sleep(0.05)

    print('Closing device')
    h.close()

except IOError as ex:
    print(ex)
    print('You probably don\'t have the hard coded test hid. Update the hid.device line')
    print('in this script with one from the enumeration list output above and try again.')

print('Done')
