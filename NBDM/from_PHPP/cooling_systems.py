# -*- coding: utf-8 -*-
# -*- Python Version: 3.7 -*-

"""Functions to create NBDM Cooling Systems from PHPP."""

from PHX.PHPP.phpp_app import PHPPConnection

from NBDM.model.cooling_systems import NBDM_BuildingSegmentCoolingSystems


def create_NBDM_Cooling_Systems(
    _phpp_conn: PHPPConnection,
) -> NBDM_BuildingSegmentCoolingSystems:
    """Read in data from a PHPP document and create a new NBDM_BuildingSegmentCoolingSystems Object."""

    return NBDM_BuildingSegmentCoolingSystems()
