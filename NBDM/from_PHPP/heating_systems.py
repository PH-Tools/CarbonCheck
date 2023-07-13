# -*- coding: utf-8 -*-
# -*- Python Version: 3.7 -*-

"""Functions to create NBDM Heating Systems from PHPP."""

from PHX.PHPP.phpp_app import PHPPConnection

from NBDM.model.heating_systems import NBDM_BuildingSegmentHeatingSystems


def create_NBDM_Heating_Systems(
    _phpp_conn: PHPPConnection,
) -> NBDM_BuildingSegmentHeatingSystems:
    """Read in data from a PHPP document and create a new NBDM_BuildingSegmentHeatingSystems Object."""

    return NBDM_BuildingSegmentHeatingSystems()
