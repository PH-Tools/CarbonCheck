# -*- mode: python ; coding: utf-8 -*-
# To Build: PyInstaller CarbonCheck.spec  #-- REMEMBER: Capitalize PyInstaller!!

block_cipher = None

a = Analysis(
    ['CarbonCheck.py'],
    pathex=[],
    binaries=[],
    datas=[
        ("/Users/em/Dropbox/bldgtyp-00/00_PH_Tools/CarbonCheck/.venv/lib/python3.11/site-packages/honeybee_energy", "honeybee_energy"),
        ("/Users/em/Dropbox/bldgtyp-00/00_PH_Tools/CarbonCheck/.venv/lib/python3.11/site-packages/honeybee_standards", "honeybee_standards"),
        ("/Users/em/Dropbox/bldgtyp-00/00_PH_Tools/CarbonCheck/.venv/lib/python3.11/site-packages/ladybug", "ladybug"),
        ("/Users/em/Dropbox/bldgtyp-00/00_PH_Tools/CarbonCheck/.venv/lib/python3.11/site-packages/honeybee", "honeybee"),
        ("/Users/em/Dropbox/bldgtyp-00/00_PH_Tools/CarbonCheck/.venv/lib/python3.11/site-packages/PHX", "PHX"),
        ("/Users/em/Dropbox/bldgtyp-00/00_PH_Tools/CarbonCheck/.venv/lib/python3.11/site-packages/ph_units", "ph_units"),
        ("/Users/em/Dropbox/bldgtyp-00/00_PH_Tools/CarbonCheck/.venv/lib/python3.11/site-packages/honeybee_ph", "honeybee_ph"),
        ("/Users/em/Dropbox/bldgtyp-00/00_PH_Tools/CarbonCheck/.venv/lib/python3.11/site-packages/honeybee_energy_ph", "honeybee_energy_ph"),
        ("/Users/em/Dropbox/bldgtyp-00/00_PH_Tools/CarbonCheck/.venv/lib/python3.11/site-packages/ladybug_geometry", "ladybug_geometry"),
        ("/Users/em/Dropbox/bldgtyp-00/00_PH_Tools/CarbonCheck/.venv/lib/python3.11/site-packages/ladybug_geometry_polyskel", "ladybug_geometry_polyskel"),
        ("/Users/em/Dropbox/bldgtyp-00/00_PH_Tools/CarbonCheck/.venv/lib/python3.11/site-packages/honeybee_ph_utils", "honeybee_ph_utils"),
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
