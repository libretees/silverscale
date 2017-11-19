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

.. code-block:: bash

    # apt-get update
    # apt-get install -y libudev-dev python-dev python3-dev
    $ wget http://sourceforge.net/projects/libusb/files/libusb-1.0/libusb-1.0.19/libusb-1.0.19.tar.bz2
    $ tar -vxjf libusb-1.0.19.tar.bz2 
    $ cd libusb-1.0.19/
    $ ./configure && make && sudo make install
    $ pip install cython
    $ pip install --global-option=build_ext --global-option='-I/usr/local/include/libusb-1.0/' hidapi
