# -*- coding: utf-8 -*-
# -*- Python Version: 3.7 -*-

"""Functions to create NBDM Appliances from PHPP."""

from PHX.PHPP.phpp_app import PHPPConnection

from NBDM.model.appliances import NBDM_BuildingSegmentAppliances


def create_NBDM_Appliances(_phpp_conn: PHPPConnection) -> NBDM_BuildingSegmentAppliances:
    """Read in data from a PHPP document and create a new NBDM_BuildingSegmentAppliances Object."""
    # area_appliances = _phpp_conn.overview.get_area_appliances()
    # area_tfa = _phpp_conn.overview.get_area_tfa()
    # vol_vn50 = _phpp_conn.overview.get_net_interior_volume()

    return NBDM_BuildingSegmentAppliances()
