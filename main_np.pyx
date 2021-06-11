# This demo prints a message to the console, and also opens a Win32 message box
# It also attempts to import numpy, which won't work unless you have numpy and
# all its stdlib dependencies in the distribution folder.

cdef extern int MessageBoxA(long hwnd, char* text, char* caption, unsigned int type )

import numpy

print ("Hello world msgbox active", numpy)

MessageBoxA(0, f"Greetings from Python: {numpy}".encode(), "Hello World!".encode(), 0)

print ("Goodbye!")