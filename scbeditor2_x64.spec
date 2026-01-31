# -*- mode: python ; coding: utf-8 -*-

import os

project_root = os.getcwd()

block_cipher = None

a = Analysis(
    ['scbeditor2.py'],
    pathex=[
        project_root,
        os.path.join(project_root, "src")
    ],
    binaries=[],
    datas=[],
    hiddenimports=['PIL._tkinter_finder'],
    hookspath=[],
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
    optimize=1
)
pyz = PYZ(
    a.pure,
    a.zipped_data,
    cipher=block_cipher
)

a.datas += [('ScbEditorII_T_16x16.png','./images/ScbEditorII_T_16x16.png', "DATA")]
a.datas += [('ScbEditorII_b_T_81x81.png','./images/ScbEditorII_b_T_81x81.png', "DATA")]
a.datas += [('openfile_b_T_81x81.png','./images/openfile_b_T_81x81.png', "DATA")]
a.datas += [('reloadfile_b_T_81x81.png','images\\reloadfile_b_T_81x81.png', "DATA")]
a.datas += [('savefile_b_T_81x81.png','./images/savefile_b_T_81x81.png', "DATA")]
a.datas += [('color-pallet_b_T_81x81.png','./images/color-pallet_b_T_81x81.png', "DATA")]
a.datas += [('curseur_b_T_81x81.png','./images/curseur_b_T_81x81.png', "DATA")]
a.datas += [('preferences_b_T_81x81.png','./images/preferences_b_T_81x81.png', "DATA")]
a.datas += [('fr_France_T_81x81.png','./images/fr_France_T_81x81.png', "DATA")]
a.datas += [('error_T_81x81.png','./images/error_T_81x81.png', "DATA")]
a.datas += [('question2_T_81x81.png','./images/question2_T_81x81.png', "DATA")]
a.datas += [('Warning_T_81x81.png','./images/Warning_T_81x81.png', "DATA")]
a.datas += [('Arrow_Right_T_16x16.png','./images/Arrow_Right_T_16x16.png', "DATA")]
a.datas += [('Arrow_Left_T_16x16.png','./images/Arrow_Left_T_16x16.png', "DATA")]
a.datas += [('Arrow_Up_T_16x16.png','./images/Arrow_Up_T_16x16.png', "DATA")]
a.datas += [('Arrow_Down_T_16x16.png','./images/Arrow_Down_T_16x16.png', "DATA")]
a.datas += [('scbeditor2_version.txt','scbeditor2_version.txt', "DATA")]

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [('O', None, 'OPTION')],
    name='scbeditor2',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=False,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None
)
