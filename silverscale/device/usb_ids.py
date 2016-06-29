#!/usr/bin/python
# -*- coding: utf-8 -*-

USB_IDS = {
    0x0b67: {
        'name': 'Fairbanks Scales',
        'devices': {
            0x555e: 'SCB-R9000'
        }
    },
    0x0eb8: {
        'name': 'Mettler Toledo',
        'devices': {
            0x2200: 'Ariva Scale',
            0xf000: 'PS60 Scale'
        }
    },
    0x0922: {
        'name': 'Dymo-CoStar Corp.',
        'devices': {
            0x8003: 'M10 10 lb Digital Postal Scale',
            0x8004: 'M25 25 lb Digital Postal Scale',
            0x8005: 'M5 5 lb Digital Postal Scale',
            0x8007: 'S100 100 lb Digital Shipping Scale',
            0x8009: 'S250 250 lb Digital Shipping Scale',
            0x800b: 'S400 400 lb Digital Shipping Scale'
        }
    },
    0x1446: {
        'name': 'X.J.GROUP',
        'devices': {
            0x6a73: 'Stamps.com Model 510 5LB Scale',
            0x6a78: 'DYMO Endicia 75lb Digital Scale'
        }
    },
    0x2233: {
        'name': 'RadioShack Corporation',
        'devices': {
            0x6323: 'USB Electronic Scale'
        }
    },
    0x2474: {
        'name': 'Stamps.com',
        'devices': {
            0x0550: 'Stainless Steel 5 lb. Digital Scale',
            0x3550: 'Stainless Steel 35 lb. Digital Scale'
        }
    },
    0x6096: {
        'name': 'SANFORD',
        'devices': {
            0x0158: 'Dymo 10 lb USB Postal Scale'
        }
    },
    0x7b7c: {
        'name': 'XM',
        'devices': {
            0x0100: 'Elane UParcel 30lb'
        }
    }
}

SUPPORTED_DEVICES = {
    (vendor_id, device_id): '%s %s' % (vendor_info.get('name'), device_name)
    for vendor_id, vendor_info in USB_IDS.items()
    for device_id, device_name in vendor_info.get('devices',{}).items()
}

