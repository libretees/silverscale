silverscale
===========

.. contents::

Dependencies
------------

    * libusb (http://libusb.info/)
    * libudev (http://www.freedesktop.org/wiki/Software/systemd/)
    * hidapi (https://github.com/trezor/cython-hidapi)

Dependency Installation
-----------------------

    # apt-get install libudev-dev
    $ wget http://sourceforge.net/projects/libusb/files/libusb-1.0/libusb-1.0.19/libusb-1.0.19.tar.bz2
    $ tar -vxjf libusb-1.0.19.tar.bz2 
    $ cd libusb-1.0.19/
    # ./configure && make && make install
    $ pip install --global-option=build_ext --global-option='-I/usr/local/include/libusb-1.0/' hidapi
