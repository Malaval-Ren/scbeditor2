# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(['scbeditor2.py'],
            pathex=['/home/renaud/Documents/scbeditor2', '/home/renaud/Documents/scbeditor2/src'],
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
            name='scbeditor2',
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
            version='scbeditor2_version.txt',
            name='scbeditor2')
