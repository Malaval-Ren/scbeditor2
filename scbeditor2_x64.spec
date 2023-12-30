# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

#           pathex=['/media/renaud/tempo/Linux - NeXTStep/Python'],
#           pathex=['/media/ysee/RMa/Personnel Privée/Python'],
#           pathex=['/Users/renaud/Documents/Python'],
#           pathex=['G:\\DEV\\Python\\Control_M221_Di-Do\\Control_M221_Di-Do'],

a = Analysis(['Control_M221_Di-Do.py'],
            pathex=['/home/renaud/Documents/Control_M221_DI-DO', '/home/renaud/Documents/Control_M221_DI-DO/src'],
            binaries=[],
            datas=[],
            hiddenimports=[],
            hookspath=[],
            runtime_hooks=[],
            excludes=[],
            win_no_prefer_redirects=False,
            win_private_assemblies=False,
            cipher=block_cipher,
            noarchive=False)
pyz = PYZ(a.pure, a.zipped_data,
            cipher=block_cipher)
exe = EXE(pyz,
            a.scripts,
            [],
            exclude_binaries=True,
            name='Control_M221_Di-Do',
            debug=False,
            bootloader_ignore_signals=False,
            strip=False,
            upx=False,
            console=False )
coll = COLLECT(exe,
            a.binaries,
            a.zipfiles,
            a.datas,
            strip=False,
            upx=False,
            upx_exclude=[],
            icon='appIcon_x64_T_256x256.gif',
            version='Control_M221_Di-Do_version.txt',
            name='Control_M221_Di-Do')
