#!/usr/bin/env python
from distutils.core import setup

setup(
    name = 'silverscale',
    packages = [
        'silverscale', 'silverscale.device', 'silverscale.reports'
    ],
    version = '0.3.7',
    description = 'Retrieve data from HID USB Scales.',
    author = 'Jared Contrascere',
    author_email = 'jcontra@gmail.com',
    url = 'https://github.com/libretees/silverscale',
    install_requires=['pyusb'],
    classifiers=[
          'Development Status :: 3 - Alpha',
          'Intended Audience :: Developers',
          'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
          'Operating System :: MacOS :: MacOS X',
          'Operating System :: Unix',
          'Operating System :: POSIX',
          'Programming Language :: Python',
          'Programming Language :: Python :: 3.4',
          'Topic :: Software Development',
          'Topic :: Software Development :: Libraries',
          'Topic :: Software Development :: Libraries :: Python Modules',
    ],
)
