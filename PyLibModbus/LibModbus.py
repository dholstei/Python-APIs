'''
libmodbus is an Open Source library to communicate with Modbus devices:

    RTU (serial) and TCP (Ethernet) support
    available for Linux (packaged), FreeBSD, Mac OS and Windows
    written in C
    great test coverage and documentation
    security audits
    no dependencies
'''

import ctypes
import sys
from PyQt5.QtWidgets import (
    QApplication, 
    QFileDialog
)
from numpy import array
# import MessageBox as M
import utils

libModbus = None

if utils.os == 'Linux':
    if utils.x64: libPath = "/usr/local/lib64/libmodbus.so"
    else: libPath = "/usr/local/lib/libmodbus.so"
else:
    libPath = "FIXME"
LibModbus = None

def SetLibXmlPath(path: str):
    global libPath
    libPath = path

def modbus_new_rtu (device: str, baud: int, parity: str, data_bit: int, stop_bit: int) -> ctypes.c_void_p:
    '''
    Description
    The modbus_new_rtu() function shall allocate and initialize a modbus_t structure to communicate in RTU mode on a serial line.

    The device argument specifies the name of the serial port handled by the OS, eg. "/dev/ttyS0" or "/dev/ttyUSB0". On Windows, it's necessary to prepend COM name with "\.\" for COM number greater than 9, eg. "\\.\COM10". See http://msdn.microsoft.com/en-us/library/aa365247(v=vs.85).aspx for details

    The baud argument specifies the baud rate of the communication, eg. 9600, 19200, 57600, 115200, etc.

    The parity argument can have one of the following values:

    N for none
    E for even
    O for odd
    The data_bits argument specifies the number of bits of data, the allowed values are 5, 6, 7 and 8.

    The stop_bits argument specifies the bits of stop, the allowed values are 1 and 2.

    Once the modbus_t structure is initialized, you must set the slave of your device with modbus_set_slave and connect to the serial bus with modbus_connect.

    Return value
    The function shall return a pointer to a modbus_t structure if successful. Otherwise it shall return NULL and set errno to one of the values defined below.
    '''
    
    global libModbus
# Load DLL into memory. 
    if libModbus == None:
        global libPath
        if utils.os == 'Linux': libModbus = ctypes.CDLL (libPath)
        else: libModbus = ctypes.WinDLL (libPath)

# set up prototype
    libModbus.modbus_new_rtu.restype = ctypes.c_void_p # correct return type
    libModbus.modbus_new_rtu.argtypes = ctypes.c_char_p, ctypes.c_int, ctypes.c_char, ctypes.c_int, ctypes.c_int

# wrapping in c_char_p or c_int32 isn't required because .argtypes are known.
    ctxt = libModbus.modbus_new_rtu(device.encode(), baud, ctypes.c_char(ord(parity)), data_bit, stop_bit)
    if ctxt == 0: raise LibErr()
    return ctxt # 

def modbus_set_slave (ctx: ctypes.c_void_p, slave: int) -> ctypes.c_int:
    '''
    Description
    The modbus_set_slave() function shall set the slave number in the libmodbus context.

    The behavior depends of network and the role of the device:

    RTU:: Define the slave ID of the remote device to talk in master mode or set the internal slave ID in slave mode. According to the protocol, a Modbus device must only accept message holding its slave number or the special broadcast number.

    TCP:: The slave number is only required in TCP if the message must reach a device on a serial network. Some not compliant devices or software (such as modpoll) uses the slave ID as unit identifier, that's incorrect (cf page 23 of Modbus Messaging Implementation Guide v1.0b) but without the slave value, the faulty remote device or software drops the requests! The special value MODBUS_TCP_SLAVE (0xFF) can be used in TCP mode to restore the default value.

    The broadcast address is MODBUS_BROADCAST_ADDRESS. This special value must be use when you want all Modbus devices of the network receive the request.

    Return value
    The function shall return 0 if successful. Otherwise it shall return -1 and set errno to one of the values defined below.
    '''
    
    global libModbus
# Load DLL into memory. 
    if libModbus == None: raise NullDLL()

# set up prototype
    libModbus.modbus_set_slave.restype = ctypes.c_int # correct return type
    libModbus.modbus_set_slave.argtypes = ctypes.c_void_p, ctypes.c_int,

# wrapping in c_char_p or c_int32 isn't required because .argtypes are known.
    rc = libModbus.modbus_set_slave(ctx, slave)
    if rc: raise LibErr("couldn't set slave")
    return rc # 

class NullDLL(Exception):
    """Exception raised if "LibModbus = None"

    Attributes:
        message -- explanation of the error
    """

    def __init__(self, message="DLL not loaded"):
        self.message = message
        super().__init__(self.message)

class libNullPtr(Exception):
    """Exception raised if "xmlDocPtr = NULL"

    Attributes:
        message -- explanation of the error
    """

    def __init__(self, message="modbus context pointer may not be NULL"):
        self.message = message
        super().__init__(self.message)

class LibErr(Exception):
    """Exception raised if "ctxt = NULL"

    Attributes:
        message -- explanation of the error
    """

    def __init__(self, message="Unable to create the libmodbus context"):
        self.message = message
        super().__init__(self.message)

def test():
    app = QApplication(sys.argv)
    FileObj = QFileDialog.getOpenFileName(None, "Select device", "/dev", None)

    if len(FileObj[0]) > 0:
        ctx = modbus_new_rtu("da fuk", 115200, 'N', 0, 0)
        ctx = modbus_new_rtu(FileObj[0], 1, 'N', 0, 0)
        rc = modbus_set_slave(ctx, 1)

    return

test()