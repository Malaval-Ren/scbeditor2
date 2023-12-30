# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

#           pathex=['/media/renaud/tempo/Linux - NeXTStep/Python'],
#           pathex=['/media/ysee/RMa/Personnel Privée/Python'],
#           pathex=['/Users/renaud/Documents/Python'],
#           pathex=['G:\\DEV\\Python\\Control_M221_DI-DO_v2=v501_to'],
#           pathex=['/Users/renaud/Documents/Python/v2 = v501 to'],
#           version='Control_M221_Di-Do_version.txt',
# a = Analysis(['Control_M221_Di-Do.py', 'src/my_configuration_data.py', 'src/my_configuration_window.py', 'src/my_icon_pictures.py', 'src/my_log_mail.py', 'src/my_main_window.py,', 'src/my_modbus_protocol.py', 'src/my_tools.py'],


a = Analysis(['Control_M221_Di-Do.py'],
             pathex=['/Users/renaud/Documents/Python/Control_M221_Di-Do/Control_M221_Di-Do/'],
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
          name='Control_M221_Di-Do',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=False,
          upx_exclude=[],
          runtime_tmpdir=None,
          console=False,
          icon='appIcons_T_1024x1024.icns')
app = BUNDLE(exe,
         name='Control_M221_Di-Do.app',
         icon='appIcons_T_1024x1024.icns',
         bundle_identifier=None,
         version='1.7.11.22',
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
