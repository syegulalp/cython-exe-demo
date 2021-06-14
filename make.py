# TODO: link against MSVCRT (?) need vcruntime140.dll

# You may need to adjust this path on your system;
# it assumes Visual Studio 2019's community build tools are installed

vc_path = (
    r"%ProgramFiles(x86)%\Microsoft Visual Studio\2019\Community\VC\Auxiliary\Build"
)
win_kitpath = r"%WindowsSdkDir%Lib\%WindowsSDKVersion%um\%VSCMD_ARG_HOST_ARCH%"

import sys
from pathlib import Path
import shutil
import subprocess
import zipfile
import py_compile
import os
import site

site_packages = site.getsitepackages()


def clean_files(file_title):
    for f in (
        f"{file_title}.exp",
        f"{file_title}.lib",
        f"{file_title}.obj",
        f"{file_title}.c",
        f"{file_title}.exe",
    ):
        Path(f).unlink(missing_ok=True)


link_vcrt = True
bundle_vcrt = True

if "-nobundle" in sys.argv:
    bundle_vcrt = False

if "-novlink" in sys.argv:
    link_vcrt = False
    bundle_vcrt = False

input_file = Path("main.pyx")

for m in sys.argv:
    if m.startswith("-i:"):
        input_file = Path(m.split("-i:", 1)[1])

if not input_file.exists():
    raise FileNotFoundError(f"File {input_file} not found")

file_title = input_file.stem

embed_src = Path("embed")
dist_path = Path("dist")
exec_path = sys.base_prefix
exec_id = f"python{sys.version_info[0]}{sys.version_info[1]}"
lib_dir = Path(subprocess.__file__).parent

print("Building", input_file)

build_win = ""

if "-w" in sys.argv:
    print("Profile: Win32 application")
    build_win = "/subsystem:windows /entry:wmainCRTStartup"
else:
    print("Profile: console application")

_link_libs = [
    fr"{exec_path}\libs\{exec_id}.lib",
    fr"{win_kitpath}\User32.lib",
    fr"{win_kitpath}\Kernel32.lib",
]

link_libs = " ".join([f'"{lib}"' for lib in _link_libs])

cmds = [
    f"py -m cython --embed -3 {file_title}.pyx",
    rf'call "{vc_path}\vcvarsall.bat" x64',
    rf'cl {file_title}.c {"/MD" if link_vcrt else ""} /I "{exec_path}\include" /link {link_libs} {build_win}',
]
# /MD

if "-v" in sys.argv or "-vv" in sys.argv:
    print("Builder commands:\n")
    for c in cmds:
        print(c, "\n")

cmd = "\n".join(cmds) + "\n"

clean_files(file_title)

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

if "-vv" in sys.argv:
    print("Command output:\n")
    print(out.decode("utf-8"))

shutil.move(str(Path(f"{file_title}.exe")), dist_path)

if "-noclean" not in sys.argv:
    clean_files(file_title)

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

for m in sys.argv:
    if m.startswith("-l:"):
        lib = m.split("-l:", 1)[1]
        libs.append(lib)

z = zipfile.ZipFile(dist_path / f"{exec_id}.zip", "w")
for l in libs:
    compiled = py_compile.compile(lib_dir / l)
    z.write(
        compiled,
        l + "c",
    )
z.close()

redist = [f"{exec_id}.dll"]
if bundle_vcrt:
    redist.append("vcruntime140.dll")

for f in redist:
    shutil.copy2(Path(exec_path, f), dist_path)

with open(dist_path / f"{exec_id}._pth", "w") as f:
    f.write(f".\napp.zip\n{exec_id}.zip")

for m in sys.argv:
    if m.startswith("-lc:"):
        dir = m.split("-lc:", 1)[1]
        for s in site_packages:
            print(Path(s, dir))
            print(Path(s, dir).exists())
            if Path(s, dir).exists():
                print("ok")
                shutil.copytree(Path(s, dir), Path(dist_path, dir))
    elif m.startswith("-c:"):
        dir = m.split("-c:", 1)[1]
        shutil.copytree(dir, dist_path / dir)
    elif m.startswith("-cc:"):
        dir = m.split("-cc:", 1)[1]
        shutil.copytree(dir, dist_path / dir)
        for root, dirs, files in os.walk(dist_path):
            for d in dirs:
                if d.endswith("__pycache__"):
                    shutil.rmtree(Path(root, d))
            for f in files:
                if f.endswith(".pyc"):
                    continue
                elif f.endswith(".py"):
                    compiled = py_compile.compile(Path(root, f), Path(root, f + "c"))
                    Path(root, f).unlink()

    elif m.startswith("-cz:"):
        dir = m.split("-cz:", 1)[1]
        z = zipfile.ZipFile(dist_path / "app.zip", "w")
        xroot = Path(dir).stem
        for root, dirs, files in os.walk(dir):
            for f in files:
                if f.endswith(".pyc"):
                    continue
                if f.endswith(".py"):
                    compiled = py_compile.compile(Path(root, f))
                    z.write(compiled, Path(xroot, f + "c"))
                else:
                    z.write(Path(root, f))
        z.close()
        # TODO: copy out binary files into another hierarchy outside zip


print("Finished building", input_file)

if "-r" in sys.argv:
    print("Running", file_title)
    os.chdir(dist_path)
    subprocess.run(f"{file_title}.exe")
