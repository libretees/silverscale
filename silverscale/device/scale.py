#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
from .importer import _USBDeviceManager, USBDevice
from ..reports import *

logger = logging.getLogger(__name__)

class Scale(USBDevice):

    def __init__(self, *args, **kwargs):
        super(Scale, self).__init__(*args, **kwargs)
        self._stable = False
        self._weight = None
        self._units = None

    def __repr__(self):
        return '<%s %s' % (self.manufacturer, self.product)

    @property
    def stable(self):
        return self._stable

    @property
    def weight(self):
        return self._weight

    @property
    def units(self):
        return self._units

    def read(self):
        report_data = super(Scale, self).read(packet_size=6)
        report = None
        try:
            report = REPORT_TYPES[report_data[0]](report_data)
        except KeyError as e:
            logger.info('Malformed data received from scale (%s).', report_data)

        if isinstance(report, DataReport):
            self._stable = report.stable
            self._units = report.units
            self._weight = report.weight

        return report


class _ScaleManager(_USBDeviceManager):
    device_class = Scale


ScaleManager = _ScaleManager()
Scale._manager = ScaleManager

