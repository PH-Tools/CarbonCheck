# -*- coding: utf-8 -*-
# -*- Python Version: 3.7 -*-

"""Functions to create NBDM Appliances from PHPP."""

from ph_units.unit_type import Unit
from PHX.model.enums.elec_equip import ElectricEquipmentType
from PHX.PHPP.phpp_app import PHPPConnection

from NBDM.model.appliances import NBDM_Appliance, NBDM_BuildingSegmentAppliances
from NBDM.model.enums import appliance_type

# -- Map NBDM Appliance Types to PHX Device Types
device_map = {
    ElectricEquipmentType.DISHWASHER: appliance_type.DISHWASHER,
    ElectricEquipmentType.CLOTHES_WASHER: appliance_type.CLOTHES_WASHER,
    ElectricEquipmentType.CLOTHES_DRYER: appliance_type.CLOTHES_DRYER,
    ElectricEquipmentType.REFRIGERATOR: appliance_type.REFRIGERATOR,
    ElectricEquipmentType.FREEZER: appliance_type.FREEZER,
    ElectricEquipmentType.FRIDGE_FREEZER: appliance_type.FRIDGE_FREEZER,
    ElectricEquipmentType.COOKING: appliance_type.COOKING,
    ElectricEquipmentType.CUSTOM: appliance_type.CUSTOM,
    ElectricEquipmentType.MEL: appliance_type.MEL,
    ElectricEquipmentType.LIGHTING_INTERIOR: appliance_type.LIGHTING_INTERIOR,
    ElectricEquipmentType.LIGHTING_EXTERIOR: appliance_type.LIGHTING_EXTERIOR,
    ElectricEquipmentType.LIGHTING_GARAGE: appliance_type.LIGHTING_GARAGE,
    ElectricEquipmentType.CUSTOM_LIGHTING: appliance_type.CUSTOM_LIGHTING,
    ElectricEquipmentType.CUSTOM_MEL: appliance_type.CUSTOM_MEL,
}


def create_NBDM_Appliances(_phpp_conn: PHPPConnection) -> NBDM_BuildingSegmentAppliances:
    """Read in data from a PHPP document and create a new NBDM_BuildingSegmentAppliances Object."""
    new_obj = NBDM_BuildingSegmentAppliances()

    for phpp_elec_appliance in _phpp_conn.electricity.get_phx_elec_devices():
        # -- If not used, leave out of the Model
        if phpp_elec_appliance.quantity == 0:
            continue

        # -- Build up a new NBDM_Appliance from the PHX Device data
        new_appliance = NBDM_Appliance()
        new_appliance.appliance_type = device_map[phpp_elec_appliance.device_type]
        new_appliance.quantity = phpp_elec_appliance.quantity
        new_appliance._display_name = (
            phpp_elec_appliance.display_name or new_appliance.appliance_type.name
        )
        new_appliance.annual_energy_use = Unit(phpp_elec_appliance.energy_demand, "KWH")

        new_obj.add_appliance(new_appliance)

    return new_obj
