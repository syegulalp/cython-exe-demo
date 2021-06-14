# An example of including a code folder.
# Compile this with the following options:
# py .\make.py -i:.\main_import.pyx -c:app
# or, to generate a .zipped code folder:
# py .\make.py -i:.\main_import.pyx -cc:app

cdef extern int MessageBoxA(long hwnd, char* text, char* caption, unsigned int type )

from app import msg

MessageBoxA(0, msg.encode(), "Hello world".encode(), 0)