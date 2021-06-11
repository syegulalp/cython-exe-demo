cython --embed -3 main.pyx

call "%ProgramFiles(x86)%\Microsoft Visual Studio\2019\Community\VC\Auxiliary\Build\vcvarsall.bat" x64

cl main.c /MD /I "C:\Python38\include" /link "C:\Python38\libs\python38.lib"  "%WindowsSdkDir%Lib\%WindowsSDKVersion%um\%VSCMD_ARG_HOST_ARCH%\User32.lib" "%WindowsSdkDir%Lib\%WindowsSDKVersion%um\%VSCMD_ARG_HOST_ARCH%\Kernel32.lib"