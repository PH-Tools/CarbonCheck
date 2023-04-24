# -*- coding: utf-8 -*-
# -*- Python Version: 3.7 -*-

"""Functions to create and add new baseline PHPP components."""

from PHX.PHPP import phpp_app
from PHX.model.constructions import PhxConstructionWindow
from PHX.PHPP.phpp_model.component_glazing import GlazingRow
from PHX.PHPP.phpp_model.component_frame import FrameRow

def create_new_baseline_window_glazing(u_value: float, shgc: float) -> PhxConstructionWindow:
    """Create a new baseline PHX window construction."""
    return PhxConstructionWindow.from_total_u_value(u_value, shgc, "BASELINE: WINDOW")

def add_new_baseline_window_glazing(phpp_conn: phpp_app.PHPPConnection, 
                                    baseline_phx_window: PhxConstructionWindow
) -> str:
    """Add a new baseline PhxConstructionWindow Glazing to the PHPP Components Worksheet.
    
    Returns:
    --------
        str: The PHPP Glazing ID (ie: "01ud-MyGlass", etc..)
    """
    phpp_glazing_row = GlazingRow(phpp_conn.shape.COMPONENTS, baseline_phx_window)
    row_num = phpp_conn.components.first_empty_glazing_row_num
    phpp_glazing_id = phpp_conn.components.write_single_glazing(row_num, phpp_glazing_row)
    return phpp_glazing_id

def add_new_baseline_window_frame(phpp_conn: phpp_app.PHPPConnection, 
                                  baseline_phx_window: PhxConstructionWindow
) -> str:
    """Add a new baseline PhxConstructionWindow Frame to the PHPP Components Worksheet.
    
    Returns:
    --------
        str: The PHPP Frame ID (ie: "01ud-MyFrame", etc..)
    """
    phpp_frame_row = FrameRow(phpp_conn.shape.COMPONENTS, baseline_phx_window)
    row_num = phpp_conn.components.first_empty_frame_row_num
    phpp_frame_id = phpp_conn.components.write_single_frame(row_num, phpp_frame_row)
    return phpp_frame_id