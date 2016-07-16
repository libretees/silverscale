#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
import sys
import usb.core
import usb.util
from ..usb_ids import SUPPORTED_DEVICES

logger = logging.getLogger(__name__)

class USBDevice(object):
    def __init__(self, device):
        self._device = device
        self._reattach = False

    @property
    def manager(self):
        return self._manager()

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
        for configuration in self._device:
            for interface in configuration:
                interface_number = interface.bInterfaceNumber
                if self._device.is_kernel_driver_active(interface_number):
                    try:
                        logger.debug('Detaching USB device kernel driver...')
                        self._device.detach_kernel_driver(interface_number)
                        logger.debug('Detached USB device kernel driver.')
                    except usb.core.USBError as e:
                        sys.exit(
                            'Could not detach kernel driver from interface(%s): %s' %
                            (interface_number, str(e)))
                    else:
                        self._reattach = True

        configuration, attempts = None, 10
        while not configuration and attempts > 0:
            try:
                # Use the first/default configuration.
                logger.debug('Setting USB device configuration...')
                self._device.set_configuration()
                logger.debug('Set USB device configuration.')
                logger.debug('Claiming USB device interface...')
                usb.util.claim_interface(self._device, interface_number)
                logger.debug('Claimed USB device interface.')
            except usb.core.USBError as e:
                logger.error('Received "%s" error while trying to connect USB '
                             'device' % e.strerror)
                if e.errno == 16: # Resource busy.
                    if attempts:
                        attempts -= 1
                        print('Resetting device...')
                        self._device.reset()
                        print('Reset device.')
                    else:
                        sys.exit('The requested USB device (%s %s) is being used by '
                                 'another process.' % (self.manufacturer, self.product))
            else:
                configuration = self._device.get_active_configuration()

        # Match the first IN endpoint.
        interface = configuration[(0,0)]
        self._endpoint_in = usb.util.find_descriptor(
            interface,
            custom_match = \
            lambda e: \
                usb.util.endpoint_direction(e.bEndpointAddress) == \
                usb.util.ENDPOINT_IN)

        self._endpoint_out = usb.util.find_descriptor(
            interface,
            custom_match = \
            lambda e: \
                usb.util.endpoint_direction(e.bEndpointAddress) == \
                usb.util.ENDPOINT_OUT)

        if self not in self.manager:
            self.manager.add(self)

    def disconnect(self):
        logger.debug('Resetting USB device...')
        self._device.reset()
        logger.debug('Reset USB device.')
        logger.debug('Disposing of USB device resources...')
        usb.util.dispose_resources(self._device)
        logger.debug('Disposed of USB device resources.')

        if self._reattach:
            logger.debug('Reattaching USB device kernel driver...')
            self._device.attach_kernel_driver(0)
            logger.debug('Reattached USB device kernel driver.')

        self.manager.remove(self)

    def read(self, packet_size=None):
        if packet_size is None:
            packet_size = self._endpoint_in.wMaxPacketSize

        report = None
        while report is None:
            try:
                logger.info('Reading from USB device endpoint...')
                report = self._device.read(self._endpoint_in.bEndpointAddress,
                                           packet_size)
                logger.info('Read from USB device endpoint (%s).' % list(report))
            except usb.core.USBError as e:
                report = None

        return list(report)

    def write(self, packet):
        result = None
        if self._endpoint_out is not None:
            logger.info('Writing to USB device endpoint (%s)...' % list(packet))
            result = self._endpoint_out.write(packet)
            logger.info('Wrote %d bytes to USB device endpoint.' % result)

        return result == len(packet)


class _USBDeviceManager(object):

    device_class = USBDevice

    def __init__(self):
        devices = usb.core.find(find_all=True,
                                custom_match=
                                    lambda x: (x.idVendor, x.idProduct) in SUPPORTED_DEVICES)
        self._devices = [self.device_class(device) for device in devices]

    def __call__(self, *args, **kwargs):
        return self

    def __contains__(self, item):
        return item in self._devices

    @property
    def devices(self):
        return self._devices

    def add(self, x):
        self._devices.append(x)

    def remove(self, x):
        if x in self._devices:
            self._devices.remove(x)

    def close(self):
        for device in self._devices:
            device.disconnect()

