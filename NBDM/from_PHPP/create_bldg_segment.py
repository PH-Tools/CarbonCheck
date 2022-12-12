# -*- coding: utf-8 -*-
# -*- Python Version: 3.7 -*-

"""Functions to create NBDM BuildingSegment objects from PHPP data."""


from PHX.PHPP import phpp_app

from NBDM.from_PHPP import create_geometry, create_occupancy, create_performance
from NBDM.model import building
from NBDM.model import enums


def create_NBDM_BuildingSegment(
    _phpp_conn: phpp_app.PHPPConnection,
) -> building.NBDM_BuildingSegment:
    """Read in data from a PHPP and build up a new BuildingSegment."""

    return building.NBDM_BuildingSegment(
        segment_name=_phpp_conn.overview.get_project_name(),
        construction_type=enums.construction_type.NEW_CONSTRUCTION,
        construction_method=enums.construction_method.METHOD_A,
        geometry=create_geometry.build_NBDM_geometry(_phpp_conn),
        occupancy=create_occupancy.build_NBDM_occupancy(_phpp_conn),
        performance=create_performance.build_NBDM_performance(_phpp_conn),
    )
