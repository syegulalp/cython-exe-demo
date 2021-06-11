# This demo prints a message to the console, and also opens a Win32 message box
# It also attempts to import numpy, which won't work unless you have numpy and
# all its stdlib dependencies in the distribution folder. To make this work,
# install numpy in your vent, download the "embeddable" version of Python (the
# .zip archive), unpack that into a folder, copy the numpy folder from the venv's
# site-packages directory into that folder, and then copy the executable generated
# from this file also into that folder.

cdef extern int MessageBoxA(long hwnd, char* text, char* caption, unsigned int type )

try:
    import numpy
except:
    MessageBoxA(0, f"Numpy not found, can't continue.".encode(), "O NOZ".encode(), 0)
else:
    print ("Hello world msgbox active", numpy)
    MessageBoxA(0, f"Greetings from Python: {numpy}".encode(), "Hello World!".encode(), 0)
    print ("Goodbye!")