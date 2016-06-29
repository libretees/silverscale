#!/usr/bin/env python
# -*- coding: utf-8 -*-

from silverscale.usb_ids import SUPPORTED_DEVICES

rule_template = """# %s
SUBSYSTEM=="usb", ATTR{idVendor}=="%04x", ATTR{idProduct}=="%04x", MODE="0664", GROUP="plugdev"

"""

def create_udev_rules(filename='usb.rules'):
    with open(filename, 'w') as rules_file:
        for device_ids, device_name in SUPPORTED_DEVICES.items():
            rule = rule_template % ((device_name,) + device_ids)
            rules_file.write(rule)

if __name__ == '__main__':
    create_udev_rules(filename='silverscale-usb.rules')

