# -*- coding: utf-8 -*-
# -*- Python Version: 3.7 -*-

"""Functions to create NBDM Geometry from PHPP data."""

from PHX.PHPP import phpp_app

from NBDM.model import geometry


def build_NBDM_geometry(
    _phpp_conn: phpp_app.PHPPConnection,
) -> geometry.NBDM_BuildingSegmentGeometry:
    """Read in data from a PHPP document and create a new NBDM_BuildingSegmentGeometry Object."""
    area_envelope = _phpp_conn.overview.get_area_envelope()
    area_tfa = _phpp_conn.overview.get_area_tfa()
    vol_vn50 = _phpp_conn.overview.get_net_interior_volume()

    return geometry.NBDM_BuildingSegmentGeometry(area_envelope, area_tfa, vol_vn50)
