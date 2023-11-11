# -*- coding: utf-8 -*-
# -*- Python Version: 3.7 -*-

"""Functions to create NBDM Appliances from WUFI-PDF."""


from PHX.model.enums.elec_equip import ElectricEquipmentType

from NBDM.from_WUFI_PDF.pdf_reader_sections import PDFSectionsCollection
from NBDM.from_WUFI_PDF.pdf_sections.res_electric import (
    WufiPDF_ElectricAppliance,
    WufiPDF_ResidentialElectric,
)
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


def create_NBDM_Appliances_from_WufiPDF(
    _pdf_data: PDFSectionsCollection,
) -> NBDM_BuildingSegmentAppliances:
    """Read in data from a WUFI-PDF document and create a new 'NBDM_Appliance' Object."""
    new_obj = NBDM_BuildingSegmentAppliances()

    if appliance_data := _pdf_data.get_section(WufiPDF_ResidentialElectric):
        for appliance in appliance_data._appliances:
            new_appliance = NBDM_Appliance()
            new_appliance.appliance_type = device_map[appliance.nbdm_appliance_type]
            new_appliance.quantity = appliance.quantity
            new_appliance.annual_energy_use = appliance.annual_demand_kWh
            new_obj.add_appliance(new_appliance)

    return new_obj
