"""cx_Freeze Build configuration for Windows MSI Installer.

NOTE: be sure to --upgrade all dependencies first
"pip install -r requirements.txt --upgrade"
"python build_windows.py bdist_msi"
"""


import sys
import os
from pathlib import Path
from cx_Freeze import setup, Executable


def find_data_file(filename):
    if getattr(sys, "frozen", False):
        # The application is frozen
        datadir = os.path.dirname(sys.executable)
    else:
        # The application is not frozen
        # Change this bit to match where you store your data files:
        datadir = os.path.dirname(__file__)
    return os.path.join(datadir, filename)


# Add in all the required dependencies.
# Automatic detection should not be relied upon
build_exe_options = {
    "includes": [
        "ladybug",
        "ladybug_geometry",
        "honeybee",
        "honeybee_energy",
        "honeybee_schema",
        "honeybee_standards",
        "ph_units",
        "ph_baseliner",
        "rich",
        "xlwings",
        "honeybee_ph",
        "honeybee_ph_standards",
        "honeybee_ph_utils",
        "honeybee_energy_ph",
        "PHX",
        "yaml",
        "lxml",
        "pdfplumber",
    ],
    "excludes": ["tcl8", "tcl8.6", "tk8.6", "tkinter", "unittest"],
    "zip_include_packages": [
        "PyQt6",
    ],
    "include_files": [("CC_GUI\\resources", "resources")],
    "include_msvcr": True,
}

# base="Win32GUI" should be used only for Windows GUI app
base = "Win32GUI" if sys.platform == "win32" else None

bdist_msi_options = {
    "add_to_path": False,
    "initial_target_dir": "C:\\CarbonCheck",
}

icon_file = find_data_file(Path("CC_GUI", "resources", "logo_CarbonCheck.ico").resolve())
setup(
    name="CarbonCheck",
    version="0.1",
    description="Passive House Model Baseliner and Reporting.",
    options={
        "build_exe": build_exe_options,
        "bdist_msi": bdist_msi_options,
    },
    executables=[
        Executable(
            "CarbonCheck.py",
            copyright="Copyright (C) 2023 Passive House Accelerator",
            base=base,
            icon=icon_file,
        )
    ],
)
