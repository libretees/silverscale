#!/usr/bin/env python
# -*- coding: utf-8 -*-

import faulthandler
import logging
from importlib import import_module

logger = logging.getLogger(__name__)

faulthandler.enable()

for module_name in ('device_libusb1', 'device_pyusb1', 'device_cython_hidapi'):
    try:
        module = import_module('.' + module_name, package='silverscale.device')
        USBDevice = getattr(module, 'USBDevice')
        _USBDeviceManager = getattr(module, '_USBDeviceManager')
        break
    except ImportError as error:
        logger.info('Could not import USB library (%s).' % str(error))
else:
    raise ImportError('No USB library found.')
