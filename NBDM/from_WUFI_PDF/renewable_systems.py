# -*- coding: utf-8 -*-
# -*- Python Version: 3.7 -*-

"""Functions to create NBDM Renewable Energy Systems from WUFI-PDF."""


from NBDM.model.renewable_systems import (
    NBDM_BuildingSegmentRenewableSystems,
    NBDM_SolarDHWDevice,
    NBDM_SolarPVDevice,
)


def create_NBDM_Renewable_Systems_from_WufiPDF(
    _pdf_data,
) -> NBDM_BuildingSegmentRenewableSystems:
    """Read in data from a WUFI-PDF document and create a new NBDM_BuildingSegmentRenewableSystems Object."""
    system_obj = NBDM_BuildingSegmentRenewableSystems()

    return system_obj
