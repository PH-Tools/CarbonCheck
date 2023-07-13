# -*- coding: utf-8 -*-
# -*- Python Version: 3.7 -*-

"""Functions to create NBDM Ventilation Systems from PHPP."""

from PHX.PHPP.phpp_app import PHPPConnection

from NBDM.model.ventilation_systems import NBDM_BuildingSegmentVentilationSystems


def create_NBDM_Ventilation_Systems(
    _phpp_conn: PHPPConnection,
) -> NBDM_BuildingSegmentVentilationSystems:
    """Read in data from a PHPP document and create a new NBDM_BuildingSegmentVentilationSystems Object."""

    return NBDM_BuildingSegmentVentilationSystems()
