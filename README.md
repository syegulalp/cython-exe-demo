This is a simple example of how to compile a Cython file to a standalone executable in Windows, using Cython's `--embed` feature.

There are very few good examples of how to do this with the most recent Visual Studio toolchain, so I thought I'd make this example for all who need it.

It ought to be possible to use this as a base for a way to create simple redistributable Python applications that have no more than they need to run.

This demo requires:

* Python 3.8 or better (I haven't tested on anything less than that)
* [Visual Studio Build Tools 2019](https://visualstudio.microsoft.com/thank-you-downloading-visual-studio/?sku=BuildTools&rel=16), or [Visual Studio 2019 Community Edition](https://visualstudio.microsoft.com/downloads/) (which includes the build tools)
* Cython (The 3.0 pre-release versions work fine; they're recommended anyway)

You can install the Python requirements from `requirements.txt`.

Run `make.py` to trigger the build process, which will build the file `main.pyx`. The resulting executable, along with the Python .DLL and a minimal standard library, will be in a subdirectory named `dist`.

`make.py` takes the following command-line flags:

* `-i:<filename>`: Select which file to compile. The default is `main.pyx`.
* `-w`: Build a windowed-only version of the application (no console output).
* `-r`: Run the built `.exe` immediately after completing the build process.
* `-l:<libpath>`: Append the lib at `<libpath>` (in Python's standard library) to the standard library zipfile bundle. E.g., `-l:smtplib.py` will add `smtplib.py`. (Note that any dependencies are not automatically resolved.)
* `-c:<directory>`: Copy the contents of `<directory>` into the distribution folder. You can use this command multiple times to copy multiple directories.
* `-cc:<directory>`: Copy the contents of `<directory>` into the distribution folder. If this folder contains `.py` files they will be compiled as `.pyc` and replaced.
* `-cz:<directory>`: Copy the contents of `<directory>` into the distribution folder, but compress them into a zip file named `app`. If this folder contains `.py` files they will be compiled as `.pyc` and replaced.
* `-v`: Verbose mode. Display the commands sent to the build process.
* `-vv`: Extra verbose mode. Echo results of build commands to the console.
* `-noclean`: By default the script cleans build artifacts (e.g., the generated C file) from the directory. Use this option to leave the build artifacts in place after the script runs. (Note that any *existing* artifacts will be overwritten with each build.)
* `-novlink`: By default the executable will be linked to `VCRUNTIME140.DLL`, which will be included with the executable. This option disables that linking and does not bundle the .DLL.
* `-nobundle`: Enables the linking, but doesn't bundle `VCRUNTIME140.DLL`. Some systems may have it installed as-is. But it's generally best to bundle the .DLL for maximum compatibility.

In time I may expand this example with more switches and options to better control how the standard library and other bundled components (e.g., SQLite3) are handled.

You can also use `compile.bat` to see a minimal example of how this works.

This code is distributed under the MIT license.