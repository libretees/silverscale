import hid

class USBDevice(object):
    def __init__(self, idVendor, idProduct):
        """Low level USB device access via cython-hidapi library.

        :param idVendor: the USB "vendor ID" number, for example 0x1941.

        :type idVendor: int

        :param idProduct: the USB "product ID" number, for example 0x8021.

        :type idProduct: int

        """
        if not hid.enumerate(idVendor, idProduct):
            raise IOError("No scale connected")
        self.hid = hid.device(idVendor, idProduct)

    def read_data(self, size):
        """Receive data from the device.

        If the read fails for any reason, an :obj:`IOError` exception
        is raised.

        :param size: the number of bytes to read.

        :type size: int

        :return: the data received.

        :rtype: list(int)

        """
        result = list()
        while size > 0:
            count = min(size, 8)
            buf = self.hid.read(count)
            if len(buf) < count:
                raise IOError(
                    'pywws.device_cython_hidapi.USBDevice.read_data failed')
            result += buf
            size -= count
        return result

    def write_data(self, buf):
        """Send data to the device.

        :param buf: the data to send.

        :type buf: list(int)

        :return: success status.

        :rtype: bool

        """
        if self.hid.write(buf) != len(buf):
            raise IOError(
                'pywws.device_cython_hidapi.USBDevice.write_data failed')
        return True

