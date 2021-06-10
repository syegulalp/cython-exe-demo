# This demo prints a message to the console, and also opens a Win32 message box

cdef extern int MessageBoxA(long hwnd, char* text, char* caption, unsigned int type )

print ("Hello world msgbox active")

MessageBoxA(0, "Greetings from Python".encode(), "Hello World!".encode(), 0)