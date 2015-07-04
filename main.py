from importlib import import_module

for module_name in ('device_libusb1', 'device_pyusb1', 'device_pyusb',
                    'device_ctypes_hidapi', 'device_cython_hidapi'):
    try:
        print(module_name)
        module = import_module('silverscale.' + module_name)
        USBDevice = getattr(module, 'USBDevice')
        break
    except ImportError as error:
        print(error)
else:
    raise ImportError('No USB library found')

scale = USBDevice(0x922, 0x8004)

