# -*- mode: python ; coding: utf-8 -*-

# -- WATCH THE VERSIONS! Mac OS is super wierd. sometimes falls to old version?
# https://www.pythonguis.com/tutorials/packaging-pyqt6-applications-pyinstaller-macos-dmg/
# To Run: PyInstaller build_mac.spec  #-- REMEMBER: Capitalize PyInstaller!! (or maybe not????) - Try both

from os.path import join, abspath, dirname
from PyInstaller.utils.hooks import collect_submodules
import PyInstaller.config

block_cipher = None

root_path = abspath(join(dirname(__name__), "."))

# --
a = Analysis(
    [join(root_path, "CarbonCheck.py")],
    pathex=[join(root_path, ".venv/lib")],
    binaries=[],
    datas=[
        (join(root_path, ".venv/lib/python3.11/site-packages/ladybug"), "ladybug"),
        (join(root_path, ".venv/lib/python3.11/site-packages/ladybug_geometry"), "ladybug_geometry"),
        (join(root_path, ".venv/lib/python3.11/site-packages/ladybug_geometry_polyskel"), "ladybug_geometry_polyskel"),
        (join(root_path, ".venv/lib/python3.11/site-packages/ladybug_rhino"), "ladybug_rhino"),
        (join(root_path, ".venv/lib/python3.11/site-packages/honeybee"), "honeybee"),
        (join(root_path, ".venv/lib/python3.11/site-packages/honeybee_schema"), "honeybee_schema"),
        (join(root_path, ".venv/lib/python3.11/site-packages/honeybee_standards"), "honeybee_standards"),
        (join(root_path, ".venv/lib/python3.11/site-packages/honeybee_energy"), "honeybee_energy"),
        # -- 
        (join(root_path, ".venv/lib/python3.11/site-packages/honeybee_ph"), "honeybee_ph"),
        (join(root_path, ".venv/lib/python3.11/site-packages/honeybee_ph_standards"), "honeybee_ph_standards"),
        (join(root_path, ".venv/lib/python3.11/site-packages/honeybee_ph_utils"), "honeybee_ph_utils"),
        (join(root_path, ".venv/lib/python3.11/site-packages/honeybee_energy_ph"), "honeybee_energy_ph"),
        (join(root_path, ".venv/lib/python3.11/site-packages/PHX"), "PHX"),
        (join(root_path, ".venv/lib/python3.11/site-packages/ph_baseliner"), "ph_baseliner"),
        (join(root_path, ".venv/lib/python3.11/site-packages/ph_units"), "ph_units"),
        # -- 
        (join(root_path, "CC_GUI/resources/__logging_config__.yaml"), "resources"),
        (join(root_path, "CC_GUI/resources/cc_styles.qss"), "resources"),
        (join(root_path, "CC_GUI/resources/logo_CarbonCheck.ico"), "resources"),
        (join(root_path, "CC_GUI/resources/logo_CarbonCheck_512x512.icns"), "resources"),
        (join(root_path, "CC_GUI/resources/logo_NYSERDA.png"), "resources"),
        (join(root_path, "CC_GUI/resources/logo_PHA.png"), "resources"),
        # -- 
        (join(root_path, ".venv/lib/python3.11/site-packages/yaml"), "yaml"),
        (join(root_path, ".venv/lib/python3.11/site-packages/_yaml"), "_yaml"),
        (join(root_path, ".venv/lib/python3.11/site-packages/pydantic"), "pydantic"),
    ],
    hiddenimports=["pydantic", "PyYaml"],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

# ---
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
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)

# --- 
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

# --
app = BUNDLE(coll,
             name='CarbonCheck.app',
             icon='CC_GUI/resources/logo_CarbonCheck_512x512.icns',
             bundle_identifier=None)

# --
PyInstaller.config.CONF['workpath'] = "./build_mac"
PyInstaller.config.CONF['distpath'] = "./dist_mac"