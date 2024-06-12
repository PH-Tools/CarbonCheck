"""
cx_Freeze Build configuration for Windows MSI Installer.

The build is designed to be run from a GitHub Action (.github/workflows/build.yml) and will
automatically rebuild the application when triggered. It will create the .msi installer file within 
a "dist" folder, and add it as an artifact to the GitHub repo.

Most of the attributes (version, name) are read in from the pyproject.toml file.

For Testing only, from command-line:
NOTE: Be sure to update all dependencies before building.

>> # Build .MSI
>> python build_windows.py bdist_msi

>> # Build .EXE
>> python build_windows.py build
"""

import os
import sys
from pathlib import Path

import toml
from cx_Freeze import Executable, setup

# -----------------------------------------------------------------------------
# Read the pyproject.toml file with then various build options / attributes
pyproject = toml.load("pyproject.toml")["tool"]["cx_Freeze"]


# -----------------------------------------------------------------------------
def find_data_file(filename) -> str:
    if getattr(sys, "frozen", False):
        # The application is frozen
        data_dir = os.path.dirname(sys.executable)
    else:
        # The application is not frozen
        # Change this bit to match where you store your data files:
        data_dir = os.path.dirname(__file__)
    return os.path.join(data_dir, filename)


ICON_FILE = find_data_file(Path("CC_GUI", "resources", "logo_CarbonCheck.ico").resolve())


# -----------------------------------------------------------------------------
# Dependencies are automatically detected, but it might need fine tuning.
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
        "toml",
        "yaml",
        "lxml",
        "pdfplumber",
    ],
    "excludes": ["tcl8", "tcl8.6", "tk8.6", "tkinter", "unittest"],
    "zip_include_packages": [
        "PyQt6",
    ],
    "include_files": [("CC_GUI\\resources", "resources"), ("CC_GUI\\Logs", "Logs")],
    "include_msvcr": True,
}


# -----------------------------------------------------------------------------
# base="Win32GUI" should be used only for Windows GUI app
base = "Win32GUI" if sys.platform == "win32" else None


# -----------------------------------------------------------------------------
# Get the options for the .MSI file created
bdist_msi_options = {
    "add_to_path": pyproject["bdsist"]["msi"]["add_to_path"],
    "initial_target_dir": pyproject["bdsist"]["msi"]["initial_target_dir"],
    "target_name": pyproject["bdsist"]["msi"]["target_name"],
    "target_version": pyproject["bdsist"]["msi"]["target_version"],
}


# -----------------------------------------------------------------------------
setup(
    name=pyproject["app"]["name"],
    version=pyproject["bdsist"]["msi"]["target_version"],
    description=pyproject["app"]["description"],
    options={
        "build_exe": build_exe_options,
        "bdist_msi": bdist_msi_options,
    },
    executables=[
        Executable(
            script="CarbonCheck.py",
            copyright=pyproject["app"]["copyright"],
            base=base,
            icon=ICON_FILE,
        )
    ],
)
