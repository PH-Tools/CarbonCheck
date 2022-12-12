# -*- coding: utf-8 -*-
# -*- Python Version: 3.7 -*-

"""Functions to create NBDM Occupancy from PHPP data."""

from PHX.PHPP import phpp_app

from NBDM.model import occupancy


def build_NBDM_occupancy(
    _phpp_conn: phpp_app.PHPPConnection,
) -> occupancy.NBDM_BuildingSegmentOccupancy:
    """Read in data from a PHPP document and create a new NBDM_BuildingSegmentOccupancy Object."""
    num_dwellings = _phpp_conn.overview.get_number_of_dwellings()
    num_occupants = _phpp_conn.overview.get_number_of_occupants()

    return occupancy.NBDM_BuildingSegmentOccupancy(num_dwellings, num_occupants)
