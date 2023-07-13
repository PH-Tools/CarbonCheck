# -*- coding: utf-8 -*-
# -*- Python Version: 3.7 -*-

"""Functions to create NBDM Domestic Hot-Water (DHW) Systems from PHPP."""

from PHX.PHPP.phpp_app import PHPPConnection

from NBDM.model.dhw_systems import NBDM_BuildingSegmentDHWSystems


def create_NBDM_DHW_Systems(
    _phpp_conn: PHPPConnection,
) -> NBDM_BuildingSegmentDHWSystems:
    """Read in data from a PHPP document and create a new NBDM_BuildingSegmentDHWSystems Object."""

    return NBDM_BuildingSegmentDHWSystems()
