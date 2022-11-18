
import ctypes
x64 = ctypes.sizeof(ctypes.c_void_p) == 8
import platform
os = platform.system()