# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(
    ['scbeditor2.py'],
    pathex=['/Users/renaud/Documents/Python/scbeditor2/scbeditor2/'],
    binaries=[],
    datas=[],
    hiddenimports=[],
    hookspath=[],
    runtime_hooks=[],
    excludes=[
        'altgraph',
        'astroid',
        'dill',
        'gitdb',
        'GitPython',
        'isort',
        'macholib',
        'mccabe',
        'packaging',
        'pip',
        'platformdirs',
        'Pmw',
        'pyinstaller',
        'pyinstaller-hooks-contrib',
        'pylint',
        'pymodbus',
        'pypi',
        'PySide2',
        'pythonping',
        'setuptools',
        'shiboken2',
        'smmap',
        'tomlkit',
        'ttkthemes',
        'ttkwidgets',
        'wheel'
    ],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False
)
pyz = PYZ(
    a.pure,
    a.zipped_data,
    cipher=block_cipher
)
exe = EXE(
    pyz,
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
    icon='appIcon_T_1024x1024.icns'
)
app = BUNDLE(
    exe,
    name='scbeditor2.app',
    icon='appIcon_T_1024x1024.icns',
    bundle_identifier=None,
    version='2.9.22.119',
    info_plist={
        'NSPrincipalClass': 'NSApplication',
        'NSAppleScriptEnabled': False,
        'CFBundleDocumentTypes':
        [
            {
            'CFBundleTypeName': 'My File Format',
            'CFBundleTypeIconFile': 'appIcon_T_1024x1024.icns',
            'LSItemContentTypes': ['com.example.myformat'],
            'LSHandlerRank': 'Owner'
            }
        ]
    }
)
