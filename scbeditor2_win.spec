# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

#           pathex=['/media/renaud/tempo/Linux - NeXTStep/Python'],
#           pathex=['/media/ysee/RMa/Personnel Privée/Python'],
#           pathex=['/Users/renaud/Documents/Python'],
#           pathex=['G:\\DEV\\Python\\scbeditor2_v2=v501_to'],

a = Analysis(['scbeditor2.py'],
            pathex=['G:\\DEV\\Python\\scbeditor2\\scbeditor2'],
            binaries=[],
            datas=[],
            hiddenimports=[],
            hookspath=[],
            runtime_hooks=[],
            excludes=['pandas','numpy','altgraph','astroid','colorama','future','gitdb','GitPython','isort','lazy-object-proxy','mccabe','pefile','Pillow','pip','platformdirs','Pmw','pycodestyle','pyinstaller','pyinstaller-hooks-contrib','pylint','pypi','pyserial','PySide2','pywin32-ctypes','setuptools','shiboken2','smmap','toml','ttkthemes','ttkwidgets','typing-extensions','wrapt'],
            win_no_prefer_redirects=False,
            win_private_assemblies=False,
            cipher=block_cipher,
            noarchive=False)
pyz = PYZ(a.pure, a.zipped_data,
            cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          [],
          name='scbeditor2',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=False,
          upx_exclude=[],
          runtime_tmpdir=None,
          console=False,
          version='scbeditor2_version.txt',
          icon='scbeditor2_T_512x512.ico')
