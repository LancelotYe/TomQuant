# -*- coding: utf-8 -*-
import sys
from cx_Freeze import setup,Executable

build_exe_options={'optimize':2,'include_files':['']}
base=None

if sys.platform='win64'
base='Win64GUI'

executables=[Executable(script='xxxx.py',
base=base,
targetName='xxxxx.exe',
compress=True
)]

setup(name='xxxxx',
version='0.1',
description='Sample cs_Freeze wxPython script',
option={'build_exe':build_exe_options},
executables=executables )

