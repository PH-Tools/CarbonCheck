# -*- coding: utf-8 -*-
# -*- Python Version: 3.7 -*-

"""Functions to create NBDM BuildingSegment objects from PHPP data."""


from PHX.PHPP import phpp_app


from NBDM.from_PHPP.geometry import build_NBDM_geometry
from NBDM.from_PHPP.occupancy import build_NBDM_occupancy
from NBDM.from_PHPP.performance import build_NBDM_performance

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
        geometry=build_NBDM_geometry(_phpp_conn),
        occupancy=build_NBDM_occupancy(_phpp_conn),
        performance=build_NBDM_performance(_phpp_conn),
    )
