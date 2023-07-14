# -*- coding: utf-8 -*-
# -*- Python Version: 3.7 -*-

"""Functions to create NBDM Appliances from PHPP."""

from PHX.PHPP.phpp_app import PHPPConnection

from NBDM.model.appliances import NBDM_BuildingSegmentAppliances, NBDM_Appliance
from NBDM.model.enums import appliance_type


def create_NBDM_Appliances(_phpp_conn: PHPPConnection) -> NBDM_BuildingSegmentAppliances:
    """Read in data from a PHPP document and create a new NBDM_BuildingSegmentAppliances Object."""
    new_obj = NBDM_BuildingSegmentAppliances()

    # for phpp_appliance_data in _phpp_conn.electricity.get_all_appliances():
    #     new_appliance = NBDM_Appliance()
    #     new_obj.add_appliance(new_appliance)

    return new_obj
