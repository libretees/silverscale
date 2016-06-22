#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import usb.core
import usb.util
from silverscale.usb_ids import SUPPORTED_DEVICES



# find the USB device
# device = usb.core.find(idVendor=VENDOR_ID,
#                         idProduct=PRODUCT_ID)
class USBDevice(object):
    def __init__(self, device):
        self._device = device
        self._reattach = False

    @property
    def product(self):
        return usb.util.get_string(self._device, self._device.iProduct)

    @property
    def manufacturer(self):
        return usb.util.get_string(self._device, self._device.iManufacturer)

    @property
    def serial_number(self):
        return usb.util.get_string(self._device, self._device.iSerialNumber)

    def connect(self):
        for configuraton in self._device:
            for interface in configuraton:
                interface_number = interface.bInterfaceNumber
                if self._device.is_kernel_driver_active(interface_number):
                    try:
                        self._device.detach_kernel_driver(interface_number)
                    except usb.core.USBError as e:
                        sys.exit(
                            'Could not detach kernel driver from interface(%s): %s' %
                            (interface_number, str(e)))
                    else:
                        self._reattach = True

        # use the first/default configuration
        self._device.set_configuration()
        # first endpoint
        self._endpoint = self._device[0][(0,0)][0]

        if self not in self._manager():
            self.manager().append(self)

    def disconnect(self):
        self._device.reset()
        usb.util.dispose_resources(self._device)

        if self._reattach:
            self._device.attach_kernel_driver(0)

        self._manager().remove(self)

    def read(self, packet_size=None):
        if packet_size is None:
            packet_size = self._endpoint.wMaxPacketSize

        return self._device.read(self._endpoint.bEndpointAddress, packet_size)


class _DeviceManager(object):

    def __init__(self):
        devices = usb.core.find(find_all=True,
                                custom_match=
                                    lambda x: (x.idVendor, x.idProduct) in SUPPORTED_DEVICES)
        self._devices = [USBDevice(device) for device in devices]

    def __call__(self, *args, **kwargs):
        return self

    def __contains__(self, item):
        return item in self._devices

    @property
    def devices(self):
        return self._devices

    def remove(self, x):
        self._devices.remove(x)

    def close(self):
        for device in self._devices:
            device.disconnect()


DeviceManager = _DeviceManager()
USBDevice._manager = DeviceManager

device_manager = DeviceManager()

for device in device_manager.devices:
    device.connect()

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

