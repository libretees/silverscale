#!/bin/sh
#########################################################
# Installer for udev usb rules for Silverscale USB Scales
#########################################################

# check if root
if [ $(id -u) -ne 0 ]; then
    # escalate
    echo "\nInstaller requires root, escalating via sudo.\n"
    sudo "$0" "$@"
    exit $?
fi

echo "Linux installer script for Silverscale.\n"

CURRENT_PATH=`pwd`
cd `dirname $0`
# save installer script location
SDK_PATH=`pwd`
# return to original path
cd $CURRENT_PATH

# if not OSX, install udev rules.
if [ "`uname -s`" != "Darwin" ]; then
    echo "Installing rules for Silverscale USB Scales into /etc/udev/rules.d/"

    # Generate udev rules.
    /usr/bin/env python -m ${SDK_PATH}/silverscale/install/install_linux

    # Install UDEV rules for USB device
    if [ -f ${SDK_PATH}/silverscale-usb.rules ]; then
        cp ${SDK_PATH}/silverscale-usb.rules /etc/udev/rules.d/50-silverscale-usb.rules
        rm ${SDK_PATH}/silverscale-usb.rules
	udevadm trigger --attr-match=subsystem=usb
    else
        echo "ERROR: silverscale-usb.rules file not found."
    fi
fi

echo "Done.\n"
