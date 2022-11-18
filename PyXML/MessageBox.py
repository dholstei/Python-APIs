
# MessageBox(0, str("Stuff to display"), str("Caption-y stuff"), 0)
# MessageBox(0, "Stuff to display", "Caption-y stuff", 0)
import ctypes
import utils

libSDL = None

def MessageBox (hWnd: int, lpText: str, lpCaption: str, uType: int) -> int:
    global libSDL
# Load DLL into memory. 
    if libSDL == None:
        if utils.os == 'Linux':
            if utils.x64: libSDL = ctypes.CDLL ("/usr/lib64/libSDL2-2.0.so.0")
            else: libSDL = ctypes.CDLL ("/usr/lib/libSDL2-2.0.so.0")
        else: libSDL = ctypes.WinDLL (None) #  FIX ME

# set up prototype
    libSDL.SDL_ShowSimpleMessageBox.restype = ctypes.c_int32 # correct return type
    libSDL.SDL_ShowSimpleMessageBox.argtypes = ctypes.c_uint32, ctypes.c_char_p, ctypes.c_char_p, ctypes.c_void_p,
  
# wrapping in c_char_p or c_int32 isn't required because .argtypes are known.
    rc = libSDL.SDL_ShowSimpleMessageBox(   ctypes.c_uint32 (uType),
                                            ctypes.create_string_buffer (lpCaption.encode('utf-8')), 
                                            ctypes.create_string_buffer (lpText.encode('utf-8')), 
                                            ctypes.c_void_p (hWnd))
    return rc

# MessageBox(0, "Stuff to display", "Caption-y stuff", 0)