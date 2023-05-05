# -*- coding: utf-8 -*-
# -*- Python Version: 3.7 -*-

"""Export an HBJSON file to a PHPP excel document."""

import pathlib

import xlwings as xw

from PHX.xl import xl_app
from PHX.PHPP import phpp_app

from ph_baseliner.codes.model import BaselineCode
from ph_baseliner.codes.options import ClimateZones, PF_Groups, Use_Groups
from ph_baseliner.phpp.areas import set_baseline_envelope_constructions
from ph_baseliner.phpp.windows import (
    set_baseline_window_construction,
    set_baseline_window_area,
    set_baseline_skylight_area,
)
from ph_baseliner.phpp.lighting import set_baseline_lighting_installed_power_density

# --- Connect to open instance of XL, Load the correct PHPP Shape file
# -----------------------------------------------------------------------------
xl = xl_app.XLConnection(xl_framework=xw)
_phpp_conn = phpp_app.PHPPConnection(xl)

# --- Load the Code baseline model
# -----------------------------------------------------------------------------
baseline_code_file_path = pathlib.Path("./ph_baseliner/codes/2020_ECCCNY.json")
_baseline_code = BaselineCode.parse_file(baseline_code_file_path)

# --- Set the baseline values in the PHPP Worksheets
# -----------------------------------------------------------------------------
with _phpp_conn.xl.in_silent_mode():
    set_baseline_envelope_constructions(_phpp_conn, _baseline_code, ClimateZones.CZ4)
    set_baseline_window_construction(
        _phpp_conn,
        _baseline_code,
        ClimateZones.CZ4,
        PF_Groups.pf_under_20,
        Use_Groups.group_r,
    )
    set_baseline_window_area(_phpp_conn, _baseline_code)
    set_baseline_skylight_area(_phpp_conn, _baseline_code)
    set_baseline_lighting_installed_power_density(_phpp_conn, _baseline_code)
