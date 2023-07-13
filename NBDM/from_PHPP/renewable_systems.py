# -*- coding: utf-8 -*-
# -*- Python Version: 3.7 -*-

"""Functions to create NBDM Renewable Energy Systems from PHPP."""

from PHX.PHPP.phpp_app import PHPPConnection

from NBDM.model.renewable_systems import NBDM_BuildingSegmentRenewableSystems


def create_NBDM_Renewable_Systems(
    _phpp_conn: PHPPConnection,
) -> NBDM_BuildingSegmentRenewableSystems:
    """Read in data from a PHPP document and create a new NBDM_BuildingSegmentRenewableSystems Object."""

    return NBDM_BuildingSegmentRenewableSystems()
