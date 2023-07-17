# -*- coding: utf-8 -*-
# -*- Python Version: 3.7 -*-

"""Functions to create NBDM Ventilation Systems from PHPP."""

from PHX.PHPP.phpp_app import PHPPConnection

from NBDM.model.ventilation_systems import (
    NBDM_BuildingSegmentVentilationSystems,
    NBDM_VentilationDevice,
)


def create_NBDM_Ventilation_Systems(
    _phpp_conn: PHPPConnection,
) -> NBDM_BuildingSegmentVentilationSystems:
    """Read in data from a PHPP document and create a new NBDM_BuildingSegmentVentilationSystems Object."""
    obj = NBDM_BuildingSegmentVentilationSystems()

    for ventilation_device in _phpp_conn.addnl_vent.get_ventilation_units():
        if ventilation_device.display_name in ["None", "-", ""]:
            continue

        obj.add_device(
            NBDM_VentilationDevice(
                display_name=ventilation_device.display_name,
                vent_unit_type_name=ventilation_device.vent_unit_type_name,
                quantity=ventilation_device.quantity,
                hr_efficiency=ventilation_device.hr_efficiency,
                mr_efficiency=ventilation_device.mr_efficiency,
            )
        )

    return obj
