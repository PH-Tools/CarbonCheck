# -*- mode: python ; coding: utf-8 -*-
# To Build: PyInstaller CarbonCheck.spec  #-- REMEMBER: Capitalize PyInstaller!!

block_cipher = None

a = Analysis(
    ['CarbonCheck.py'],
    pathex=[],
    binaries=[],
    datas=[
        (".venv/lib/python3.11/site-packages/ladybug", "ladybug"),
        (".venv/lib/python3.11/site-packages/honeybee_energy", "honeybee_energy"),
        (".venv/lib/python3.11/site-packages/honeybee_standards", "honeybee_standards"),
        (".venv/lib/python3.11/site-packages/PHX/PHPP/phpp_localization/*.json", "PHX/PHPP/phpp_localization")
    ],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)
pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='CarbonCheck',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='CarbonCheck',
)
