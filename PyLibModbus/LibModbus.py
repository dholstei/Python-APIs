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

class MODBUS_RTU:
    RS232 = 0
    RS485 = 1

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

class modbus:
    ctx: ctypes.c_void_p
    errno: ctypes.c_int = 0
    def __init__(self, ctx = 0):
        self.ctx = ctx

    def __del__(self):
        '''
        Description
        The modbus_close() function shall close the connection established with the backend set in the context.
        '''
        global libModbus
    # Load DLL into memory. 
        if libModbus == None: raise NullDLL()

    # set up prototype
        libModbus.modbus_close.argtypes = ctypes.c_void_p,
        libModbus.modbus_close(self.ctx)
        self.ctx = 0
        return

    def new_rtu(self, device: str, baud: int, parity: str, data_bit: int, stop_bit: int):
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

        self.ctx = libModbus.modbus_new_rtu(device.encode(), baud, ctypes.c_char(ord(parity)), data_bit, stop_bit)
        if self.ctx == 0: raise LibErr()
        return

    def rtu_set_serial_mode (self,  mode: int) -> ctypes.c_int:
        '''
        modbus_rtu_set_serial_mode - set the serial mode
        int modbus_rtu_set_serial_mode(modbus_t *ctx, int mode);

        Description
        The modbus_rtu_set_serial_mode() function shall set the selected serial mode:

        MODBUS_RTU_RS232, the serial line is set for RS232 communication. RS-232 (Recommended Standard 232) is the traditional name for a series of standards for serial binary single-ended data and control signals connecting between a DTE (Data Terminal Equipment) and a DCE (Data Circuit-terminating Equipment). It is commonly used in computer serial ports.

        MODBUS_RTU_RS485, the serial line is set for RS485 communication. EIA-485, also known as TIA/EIA-485 or RS-485, is a standard defining the electrical characteristics of drivers and receivers for use in balanced digital multipoint systems. This standard is widely used for communications in industrial automation because it can be used effectively over long distances and in electrically noisy environments.
        #define 	MODBUS_RTU_RS232   0
        #define 	MODBUS_RTU_RS485   1
        '''
        
        global libModbus
    # Load DLL into memory. 
        if libModbus == None: raise NullDLL()

    # set up prototype
        libModbus.modbus_rtu_set_serial_mode.restype = ctypes.c_int # correct return type
        libModbus.modbus_rtu_set_serial_mode.argtypes = ctypes.c_void_p, ctypes.c_int,

        rc = libModbus.modbus_rtu_set_serial_mode(self.ctx, mode)
        if rc:  self.GetErrno()
        return rc # 

    def set_slave (self,  slave: int) -> ctypes.c_int:
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

        rc = libModbus.modbus_set_slave(self.ctx, slave)
        if rc:  self.GetErrno()
        return rc # 

    def connect (self) -> ctypes.c_int:
        '''
        Description
        The modbus_connect() function shall establish a connection to a Modbus server, a network or a bus using the context information of libmodbus context given in argument.

        Return value
        The function shall return 0 if successful. Otherwise it shall return -1 and set errno to one of the values defined by the system calls of the underlying platform.
        '''
        
        global libModbus
    # Load DLL into memory. 
        if libModbus == None: raise NullDLL()

    # set up prototype
        libModbus.modbus_connect.restype = ctypes.c_int # correct return type
        libModbus.modbus_connect.argtypes = ctypes.c_void_p,

        rc = libModbus.modbus_connect(self.ctx)
        if rc == -1: self.GetErrno()
        return rc # 

    def write_bit (self, addr: int, status: int) -> ctypes.c_int:
        '''
        Description
        The modbus_write_bit() function shall write the status of status at the address addr of the remote device. The value must be set to TRUE or FALSE.

        The function uses the Modbus function code 0x05 (force single coil).

        Return value
        The function shall return 1 if successful. Otherwise it shall return -1 and set errno.
        '''
        
        global libModbus
    # Load DLL into memory. 
        if libModbus == None: raise NullDLL()

    # set up prototype
        libModbus.modbus_write_bit.restype = ctypes.c_int # correct return type
        libModbus.modbus_write_bit.argtypes = ctypes.c_void_p, ctypes.c_int, ctypes.c_int,

    # wrapping in c_char_p or c_int32 isn't required because .argtypes are known.
        rc = libModbus.modbus_write_bit(self.ctx, addr, status)
        if rc == -1: self.GetErrno()
        return rc

    def write_bits (self, addr: int, src: bytearray) -> ctypes.c_int:
        '''
        modbus_write_bits - write many bits
        int modbus_write_bits(modbus_t *ctx, int addr, int nb, const uint8_t *src);

        Description
        The modbus_write_bits() function shall write the status of the nb bits (coils) from src at the address addr of the remote device. The src array must contains bytes set to TRUE or FALSE.

        The function uses the Modbus function code 0x0F (force multiple coils).

        Return value
        The function shall return the number of written bits if successful. Otherwise it shall return -1 and set errno.
        
        Note:  Length of bytearray used instead of nb
        '''
        global libModbus
    # Load DLL into memory. 
        if libModbus == None: raise NullDLL()

    # set up prototype
        libModbus.modbus_write_bits.restype = ctypes.c_int # correct return type
        libModbus.modbus_write_bits.argtypes = ctypes.c_void_p, ctypes.c_int, ctypes.c_int, ctypes.POINTER(ctypes.c_byte),

        rc = libModbus.modbus_write_bits(self.ctx, addr, len(src), 
                        (ctypes.c_byte*len(src)).from_buffer(bytearray(src)))
        if rc == -1: 
            self.GetErrno()
            return None
        return rc

    def read_bits (self, addr: int, nb: int) -> ctypes.POINTER(ctypes.c_byte):
        '''
        modbus_read_bits - read many bits
        int modbus_read_bits(modbus_t *ctx, int addr, int nb, uint8_t *dest);

        Description
        The modbus_read_bits() function shall read the status of the nb bits (coils) to the address addr of the remote device. The result of reading is stored in dest array as unsigned bytes (8 bits) set to TRUE or FALSE.

        You must take care to allocate enough memory to store the results in dest (at least nb * sizeof(uint8_t)).

        The function uses the Modbus function code 0x01 (read coil status).

        Return value
        The function shall return the number of read bits if successful. Otherwise it shall return -1 and set errno.
        '''
        
        global libModbus
    # Load DLL into memory. 
        if libModbus == None: raise NullDLL()
        dest = (ctypes.c_byte * nb)()

    # set up prototype
        libModbus.modbus_read_bits.restype = ctypes.c_int # correct return type
        libModbus.modbus_read_bits.argtypes = ctypes.c_void_p, ctypes.c_int, ctypes.c_int, ctypes.POINTER(ctypes.c_byte),

    # wrapping in c_char_p or c_int32 isn't required because .argtypes are known.
        rc = libModbus.modbus_read_bits(self.ctx, addr, nb, dest)
        if rc == -1: 
            self.GetErrno()
            return None
        return dest

    def read_input_bits (self, addr: int, nb: int) -> ctypes.POINTER(ctypes.c_byte):
        '''
        modbus_read_input_bits - read many input bits
        int modbus_read_input_bits(modbus_t *ctx, int addr, int nb, uint8_t *dest);

        Description
        The modbus_read_input_bits() function shall read the content of the nb input bits to the address addr of the remote device. The result of reading is stored in dest array as unsigned bytes (8 bits) set to TRUE or FALSE.

        You must take care to allocate enough memory to store the results in dest (at least nb * sizeof(uint8_t)).

        The function uses the Modbus function code 0x02 (read input status).

        Return value
        The function shall return the number of read input status if successful. Otherwise it shall return -1 and set errno.
        '''
        
        global libModbus
    # Load DLL into memory. 
        if libModbus == None: raise NullDLL()
        dest = (ctypes.c_byte * nb)()

    # set up prototype
        libModbus.modbus_read_input_bits.restype = ctypes.c_int # correct return type
        libModbus.modbus_read_input_bits.argtypes = ctypes.c_void_p, ctypes.c_int, ctypes.c_int, ctypes.POINTER(ctypes.c_byte),

    # wrapping in c_char_p or c_int32 isn't required because .argtypes are known.
        rc = libModbus.modbus_read_input_bits(self.ctx, addr, nb, dest)
        if rc == -1: 
            self.GetErrno()
            return None
        return dest

    def write_register (self, addr: int, value: ctypes.c_uint16) -> ctypes.c_int:
        '''
        modbus_write_register - write a single register
        int modbus_write_register(modbus_t *ctx, int addr, const uint16_t value);

        Description
        The modbus_write_register() function shall write the value of value holding registers at the address addr of the remote device.

        The function uses the Modbus function code 0x06 (preset single register).

        Return value
        The function shall return 1 if successful. Otherwise it shall return -1 and set errno.
        '''
        
        global libModbus
    # Load DLL into memory. 
        if libModbus == None: raise NullDLL()

    # set up prototype
        libModbus.modbus_write_register.restype = ctypes.c_int # correct return type
        libModbus.modbus_write_register.argtypes = ctypes.c_void_p, ctypes.c_int, ctypes.c_uint16,

        rc = libModbus.modbus_write_register(self.ctx, addr, value)
        if rc == -1: self.GetErrno()
        return rc

    def read_registers (self, addr: int, nb: int) -> ctypes.POINTER(ctypes.c_uint16):
        '''
        modbus_read_registers - read many registers
        int modbus_read_registers(modbus_t *ctx, int addr, int nb, uint16_t *dest);

        Description
        The modbus_read_registers() function shall read the content of the nb holding registers to the address addr of the remote device. The result of reading is stored in dest array as word values (16 bits).

        You must take care to allocate enough memory to store the results in dest (at least nb * sizeof(uint16_t)).

        The function uses the Modbus function code 0x03 (read holding registers).

        Return value
        The function shall return the number of read registers if successful. Otherwise it shall return -1 and set errno.
        '''
        
        global libModbus
    # Load DLL into memory. 
        if libModbus == None: raise NullDLL()
        dest = (ctypes.c_uint16 * nb)()

    # set up prototype
        libModbus.modbus_read_registers.restype = ctypes.c_int # correct return type
        libModbus.modbus_read_registers.argtypes = ctypes.c_void_p, ctypes.c_int, ctypes.c_int, ctypes.POINTER(ctypes.c_uint16),

    # wrapping in c_char_p or c_int32 isn't required because .argtypes are known.
        rc = libModbus.modbus_read_registers(self.ctx, addr, nb, dest)
        if rc == -1: 
            self.GetErrno()
            return None
        return dest

    def read_input_registers (self, addr: int, nb: int) -> ctypes.POINTER(ctypes.c_uint16):
        '''
        modbus_read_input_registers - read many input registers
        int modbus_read_input_registers(modbus_t *ctx, int addr, int nb, uint16_t *dest);

        Description
        The modbus_read_input_registers() function shall read the content of the nb input registers to address addr of the remote device. The result of the reading is stored in dest array as word values (16 bits).

        You must take care to allocate enough memory to store the results in dest (at least nb * sizeof(uint16_t)).

        The function uses the Modbus function code 0x04 (read input registers). The holding registers and input registers have different historical meaning, but nowadays it's more common to use holding registers only.

        Return value
        The function shall return the number of read input registers if successful. Otherwise it shall return -1 and set errno.        
        '''
        
        global libModbus
    # Load DLL into memory. 
        if libModbus == None: raise NullDLL()
        dest = (ctypes.c_uint16 * nb)()

    # set up prototype
        libModbus.modbus_read_input_registers.restype = ctypes.c_int # correct return type
        libModbus.modbus_read_input_registers.argtypes = ctypes.c_void_p, ctypes.c_int, ctypes.c_int, ctypes.POINTER(ctypes.c_uint16),

    # wrapping in c_char_p or c_int32 isn't required because .argtypes are known.
        rc = libModbus.modbus_read_input_registers(self.ctx, addr, nb, dest)
        if rc == -1: 
            self.GetErrno()
            return None
        return dest

    def GetErrno(self) -> ctypes.c_int:
        l = ctypes.CDLL ("/lib64/libc.so.6")
        self.errno = (ctypes.c_int.in_dll(l,"errno")).value
        # return ctypes.c_int.in_dll(libModbus,"errno")
        return self.errno

    def GetErrMsg(self) -> str:
        libModbus.modbus_strerror.restype = ctypes.c_char_p # correct return type
        libModbus.modbus_strerror.argtypes = ctypes.c_int,
        return (libModbus.modbus_strerror(self.errno)).decode()

class NullDLL(Exception):
    """Exception raised if "LibModbus = None"

    Attributes:
        message -- explanation of the error
    """

    def __init__(self, message="DLL not loaded"):
        self.message = message
        super().__init__(self.message)


class LibErr(Exception):
    """
    Attributes:
        message -- explanation of the error
    """

    global libModbus
    def __init__(self, errno):
        libModbus.modbus_strerror.restype = ctypes.c_char_p # correct return type
        libModbus.modbus_strerror.argtypes = ctypes.c_int,
        self.message = (libModbus.modbus_strerror(errno)).decode()
        super().__init__(self.message)

def test():
    import time
    app = QApplication(sys.argv)
    FileObj = QFileDialog.getOpenFileName(None, "Select device", "/dev", None)

    if len(FileObj[0]) > 0:
        m = modbus()
        m.new_rtu(FileObj[0], 115200, 'N', 0, 0)
        # n = modbus(m.ctx)   #   copy, not reentrant for the same object m.ctx
        if m.set_slave(0) == -1:    raise Exception(m.GetErrMsg())
        if m.rtu_set_serial_mode(MODBUS_RTU.RS232) == -1:   raise Exception(m.GetErrMsg())
        if m.connect() == -1:       raise Exception(m.GetErrMsg())
        time.sleep(0.250)
        if m.write_bit(8, 1) == -1: raise Exception(m.GetErrMsg())
        if m.write_bit(9, 1) == -1: raise Exception(m.GetErrMsg())
        
        dest = m.read_bits(8, 8)
        if dest == None:            raise Exception(m.GetErrMsg())
        for i in range(8): print(dest[i])
        print("---")
        
        if m.write_register(0, 20000) == -1:    raise Exception(m.GetErrMsg())
        
        src = bytearray([0, 0, 1, 0])
        if m.write_bits(8, src) == -1:    raise Exception(m.GetErrMsg())
        
        dest = m.read_registers(0, 2)
        if dest == None:            raise Exception(m.GetErrMsg())
        for i in range(2): print(dest[i])
        print("---")
        
    return

test()