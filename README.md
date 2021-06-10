This is a simple example of how to compile a Cython file to a standalone executable in Windows. There are very few good examples of how to do this with the most recent Visual Studio toolchain, so I thought I'd make this example for all who need it.

It ought to be possible to use this as a base for a way to create simple redistributable Python applications that have no more than they need to run.

This demo requires:

* Python 3.8 or better (I haven't tested on anything less than that)
* Visual Studio 2019 Community edition; specifically, the Visual C build tools
* Cython

> **Important:** In addition to having a Python version installed, you'll need to download the .ZIP-embeddable version of *the same version of Python used* and unpack it into a subdirectory named `embed`. This is so that the zipped copy of the standard library can be copied into the `dist` directory. For instance, the Python 3.8 version of the embeddable package can be downloaded from [https://www.python.org/ftp/python/3.8.10/python-3.8.10-embed-amd64.zip](https://www.python.org/ftp/python/3.8.10/python-3.8.10-embed-amd64.zip)

You can install the Python requirements from `requirements.txt`.

Run `make.py` to trigger the build process. The resulting executable, along with the Python .DLL and a minimal standard library, will be in a subdirectory named `dist`.

`make.py` takes the following command-line flags:

* `-w`: Build a windowed-only version of the application (no console output).
* `-r`: Run the built `.exe` immediately after completing the build process.

In time I may expand this example with more switches and options to better control how the standard library and other bundled components (e.g., SQLite3) are handled.

This code is distributed under the MIT license.