This is a simple example of how to compile a Cython file to a standalone executable in Windows. There are very few good examples of how to do this with the most recent Visual Studio toolchain, so I thought I'd make this example for all who need it.

It ought to be possible to use this as a base for a way to create simple redistributable Python applications that have no more than they need to run.

This demo requires:

* Python 3.8 or better (I haven't tested on anything less than that)
* Visual Studio 2019 Community edition; specifically, the Visual C build tools
* Cython

You can install the Python requirements from `requirements.txt`.

Run `make.py` to trigger the build process, which will build the file `.main.pyx`. The resulting executable, along with the Python .DLL and a minimal standard library, will be in a subdirectory named `dist`.

`make.py` takes the following command-line flags:

* `-w`: Build a windowed-only version of the application (no console output).
* `-r`: Run the built `.exe` immediately after completing the build process.
* `-l:<libpath>`: Append the lib at `<libpath>` (in Python's standard library) to the standard library zipfile bundle. E.g., `-l:smtplib.py` will add `smtplib.py`. (Note that any dependencies are not automatically resolved.)
* `-noclean`: By default the script cleans build artifacts (e.g., the generated C file) from the directory. Use this option to leave the build artifacts in place after the script runs. (Note that any *existing* artifacts will be overwritten with each build.)

In time I may expand this example with more switches and options to better control how the standard library and other bundled components (e.g., SQLite3) are handled.

This code is distributed under the MIT license.