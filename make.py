# You may need to adjust this path on your system;
# it assumes Visual Studio 2019's community build tools are installed

vc_path = (
    r"%ProgramFiles(x86)%\Microsoft Visual Studio\2019\Community\VC\Auxiliary\Build"
)
win_kitpath = r"%WindowsSdkDir%Lib\%WindowsSDKVersion%um\%VSCMD_ARG_HOST_ARCH%"

from pathlib import Path
import shutil
import subprocess
import sys
import zipfile
import py_compile

embed_src = Path("embed")
dist_path = Path("dist")
exec_path = sys.base_prefix

lib_dir = Path(subprocess.__file__).parent


def clean_files():
    for f in ("main.exp", "main.lib", "main.obj", "main.c", "main.exe"):
        Path(f).unlink(missing_ok=True)


build_win = ""

if "-w" in sys.argv:
    print("Building Win32 application")
    build_win = "/subsystem:windows /entry:wmainCRTStartup"
else:
    print("Building console application")

cmd = rf"""cython --embed -3 main.pyx
call "{vc_path}\vcvarsall.bat" x64
cl main.c /I "{exec_path}\include" /link "{exec_path}\libs\python38.lib" "{win_kitpath}\User32.lib" "{win_kitpath}\Kernel32.lib" {build_win}
"""

clean_files()

if dist_path.exists():
    shutil.rmtree(dist_path)
    dist_path.mkdir()

console = subprocess.Popen(
    "cmd.exe",
    shell=False,
    stdin=subprocess.PIPE,
    stdout=subprocess.PIPE,
    stderr=subprocess.PIPE,
)
out, err = console.communicate(bytes(cmd, encoding="utf8"))
print(out.decode("utf-8"))

shutil.move(str(Path("main.exe")), dist_path)

clean_files()

libs = [
    # The absolute basics
    "codecs.py",
    "io.py",
    "abc.py",
    "encodings/__init__.py",
    "encodings/aliases.py",
    "encodings/cp437.py",
    "encodings/cp1252.py",
    "encodings/latin_1.py",
    "encodings/utf_8.py",
    # Everything after this is needed for the site module
    "site.py",
    "os.py",
    "stat.py",
    "ntpath.py",
    "genericpath.py",
    "_collections_abc.py",
    "_sitebuiltins.py",
]

z = zipfile.ZipFile(dist_path / "python38.zip", "w")
for l in libs:
    compiled = py_compile.compile(lib_dir / l)
    z.write(
        compiled,
        l + "c",
    )
z.close()

for f in ("python38.dll",):
    shutil.copy2(embed_src / f, dist_path)

with open(dist_path / "python38._pth", "w") as f:
    f.write("python38.zip")

if "-r" in sys.argv:
    subprocess.run(dist_path / "main.exe")