# -*- coding: utf-8 -*-
# -*- Python Version: 3.7 -*-

"""Functions to create NBDM BuildingSegment objects from PHPP data."""


from PHX.PHPP import phpp_app

from NBDM.from_PHPP import create_bldg_segment
from NBDM.model import building
from NBDM.model import enums


def create_NBDM_Building(
    _phpp_conn: phpp_app.PHPPConnection,
) -> building.NBDM_Building:
    """Read in data from a PHPP and build up a new NBDM_Building with a single Segment."""

    nbdm_bldg = building.NBDM_Building(
        building_name="", building_type=enums.building_type.MULTIFAMILY
    )
    nbdm_bldg.add_building_segment(
        create_bldg_segment.create_NBDM_BuildingSegment(_phpp_conn)
    )

    return nbdm_bldg
