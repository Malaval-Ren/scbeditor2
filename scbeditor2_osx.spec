# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(['scbeditor2.py'],
             pathex=['/Users/renaud/Documents/Python/scbeditor2/scbeditor2/'],
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
          icon='appIcons_T_1024x1024.icns')
app = BUNDLE(exe,
         name='scbeditor2.app',
         icon='appIcons_T_1024x1024.icns',
         bundle_identifier=None,
         version='2.0.2.13',
         info_plist={
            'NSPrincipalClass': 'NSApplication',
            'NSAppleScriptEnabled': False,
            'CFBundleDocumentTypes': [
                {
                    'CFBundleTypeName': 'My File Format',
                    'CFBundleTypeIconFile': 'appIcons_T_1024x1024.icns',
                    'LSItemContentTypes': ['com.example.myformat'],
                    'LSHandlerRank': 'Owner'
                    }
                ]
            },
         )
