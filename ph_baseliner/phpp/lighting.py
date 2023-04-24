# -*- coding: utf-8 -*-
# -*- Python Version: 3.7 -*-

"""Functions to set baseline PHPP windows."""

from PHX.PHPP.phpp_app import PHPPConnection

from ph_baseliner.codes.model import BaselineCode
from ph_baseliner.codes.lighting_space_types import space_type_map

def find_lighting_installed_power(_baseline_code: BaselineCode, _program_name: str) -> float:
    """Find the baseline lighting installed power density for a given PHPP space."""

    # -- First, find the building-code name for the PHPP space type
    code_name = space_type_map.get(_program_name, None)

    if not code_name:
        msg = f"Error: The PHPP Space-Type name {_program_name} does not have a "\
                "corresponding building-code name?"
        raise Exception(msg)

    # -- Then, find the lighting installed power density for that building-code name
    return _baseline_code.tables.lighting_area_method.LPD[code_name]

def set_baseline_lighting_installed_power_density(_phpp_conn: PHPPConnection, _baseline_code: BaselineCode):
    """Set the PHPP 'Electricity non-res' worksheet baseline lighting installed power density.

    Arguments:
    ----------
        _phpp_conn: phpp_app.PHPPConnection
            The PHPPConnection object
        _baseline_code: BaselineCode
            The BaselineCode object
    """
    
    for row_num in _phpp_conn.elec_non_res.lighting.used_lighting_row_numbers:
        row_data = _phpp_conn.elec_non_res.lighting.get_lighting_row_data(row_num)
        code_LPD = find_lighting_installed_power(_baseline_code, row_data.utilization_profile_name)
        _phpp_conn.elec_non_res.lighting.set_lighting_power_density(row_num, code_LPD)