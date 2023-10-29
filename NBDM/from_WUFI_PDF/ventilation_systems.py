# -*- coding: utf-8 -*-
# -*- Python Version: 3.7 -*-

"""Functions to create NBDM Ventilation Systems from WUFI-PDF."""


from NBDM.model.ventilation_systems import (
    NBDM_BuildingSegmentVentilationSystems,
    NBDM_VentilationDevice,
)


def create_NBDM_Vent_Systems_from_WufiPDF(
    _pdf_data,
) -> NBDM_BuildingSegmentVentilationSystems:
    """Read in data from a WUFI-PDF document and create a new NBDM_BuildingSegmentVentilationSystems Object."""
    obj = NBDM_BuildingSegmentVentilationSystems()

    return obj
