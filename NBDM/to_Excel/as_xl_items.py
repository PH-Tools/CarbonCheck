# -*- coding: utf-8 -*-
# -*- Python Version: 3.7 -*-

"""Schemas to convert NBDM Objects into Excel Report writable items."""

from dataclasses import dataclass
from typing import Optional, List, Union, Dict, Tuple
from enum import Enum

from NBDM.model import project, building
from NBDM.to_Excel.xl_data import XlItem

COLOR_BACKGROUND_DATA = None
COLOR_BACKGROUND_HEADING_1 = (220, 220, 220)
COLOR_BACKGROUND_HEADING_2 = (100, 100, 100)
COLOR_FONT_DATA = (0, 0, 0)
COLOR_FONT_HEADING_1 = (0, 0, 0)
COLOR_FONT_HEADING_2 = (255, 255, 255)

# -----------------------------------------------------------------------------
# TODO: Move this part to another module...

project_attributes = {
    "NBDM_Project": (
        ("Project Name", "project_name"),
        ("Client", "client"),
        ("SalesForce Number", "salesforce_num"),
        ("Report Date", "report_date"),
        ("NYC ECC Year", "nyc_ecc_year"),
        ("Historic Preservation Site", "historic_preservation_site"),
        ("Disadvantaged Communities", "disadvantaged_communities"),
        ("Site", "site"),
        ("Team", "team"),
    ),
    "NBDM_Team": (
        ("Owner", "site_owner"),
        ("Designer", "designer"),
        ("Contractor", "contractor"),
        ("Primary Energy Consultant", "primary_energy_consultant"),
    ),
    "NBDM_TeamMember": (
        ("Name", "name"),
        ("Contact", "contact_info"),
    ),
    "NBDM_TeamContactInfo": (
        ("Num.", "building_number"),
        ("Street", "street_name"),
        ("City", "city"),
        ("State", "state"),
        ("Zip", "zip_code"),
        ("Phone", "phone"),
        ("Email", "email"),
    ),
    "NBDM_Site": (
        ("Climate", "climate"),
        ("Location", "location"),
    ),
    "NBDM_Location": (
        ("Longitude", "longitude"),
        ("Latitude", "latitude"),
        ("Address", "address"),
    ),
    "NBDM_ProjectAddress": (
        ("Number", "number"),
        ("Street", "street"),
        ("City", "city"),
        ("State", "state"),
        ("Zip_code", "zip_code"),
    ),
    "NBDM_Climate": (
        ("ASHRAE CZ", "zone_ashrae"),
        ("Passive House CZ", "zone_passive_house"),
        ("Climate Data Source", "source"),
    ),
    "NBDM_Variants": (),
}

bldg_attributes = {
    "NBDM_Building": (
        ("Building Name", "building_name"),
        ("Building Type", "building_type"),
        ("Geometry", "geometry"),
        ("Occupancy", "occupancy"),
        ("Performance", "performance"),
    ),
    "NBDM_BuildingSegmentGeometry": (
        ("Envelope Area", "area_envelope"),
        ("Gross Floor Area", "area_floor_area_gross"),
        ("Net Interior Floor Area", "area_floor_area_net_interior_weighted"),
        ("Interior Parking Floor Area", "area_floor_area_interior_parking"),
        ("Gross Volume", "volume_gross"),
        ("Net Interior Volume", "volume_net_interior"),
        ("Num. Stories", "total_stories"),
        ("Num. Stories Above Grade", "num_stories_above_grade"),
        ("Num. Stories Below Grade", "num_stories_below_grade"),
    ),
    "NBDM_BuildingSegmentOccupancy": (
        ("Total Dwelling Units", "total_dwelling_units"),
        ("Num. Studio", "num_apartments_studio"),
        ("Num. 1Br", "num_apartments_1_br"),
        ("Num. 2Br", "num_apartments_2_br"),
        ("Num. 3Br", "num_apartments_3_br"),
        ("Num. 4Br", "num_apartments_4_br"),
        ("Total Num. Occupants", "total_occupants"),
    ),
    "NBDM_BuildingSegmentPerformance": (
        ("Annual Energy Cost (USD)", "energy_cost"),
        ("Annual Site (End) Energy", "site_energy"),
        ("Annual Source (Primary) Energy", "source_energy"),
        ("Annual Heating Demand", "annual_heating_energy_demand"),
        ("Annual Cooling Demand", "annual_cooling_energy_demand"),
        ("Peak Heating Load", "peak_heating_load"),
        ("Peak Cooling Load", "peak_sensible_cooling_load"),
    ),
    "NBDM_SiteEnergy": (
        ("Consumption: Gas", "consumption_gas"),
        ("Consumption: Electricity", "consumption_electricity"),
        ("Consumption: District Energy", "consumption_district_heat"),
        ("Consumption: Other", "consumption_other"),
        ("Production: Solar PV", "production_solar_photovoltaic"),
        ("Production Solar Thermal", "production_solar_thermal"),
        ("Production Other", "production_other"),
    ),
    "NBDM_SourceEnergy": (
        ("Consumption: Gas", "consumption_gas"),
        ("Consumption: Electricity", "consumption_electricity"),
        ("Consumption: District Energy", "consumption_district_heat"),
        ("Consumption: Other", "consumption_other"),
        ("Production: Solar PV", "production_solar_photovoltaic"),
        ("Production Solar Thermal", "production_solar_thermal"),
        ("Production Other", "production_other"),
    ),
    "NBDM_EnergyCost": (
        ("Cost: Gas", "cost_gas"),
        ("Cost: Electricity", "cost_electricity"),
        ("Cost: District Energy", "cost_district_heat"),
        ("Cost: Other", "cost_other_energy"),
    ),
    "NBDM_AnnualHeatingDemandEnergy": (
        ("Heating Demand", "annual_demand"),
        ("Transmission Losses", "losses_transmission"),
        ("Ventilation Losses", "losses_ventilation"),
        ("Solar Gain", "gains_solar"),
        ("Internal Gains", "gains_internal"),
        ("Utilization Pattern", "utilization_factor"),
        ("Useful Gains", "gains_useful"),
    ),
    "NBDM_AnnualCoolingDemandEnergy": (
        ("Cooling Demand", "annual_demand"),
        ("Transmission Losses", "losses_transmission"),
        ("Ventilation Losses", "losses_ventilation"),
        ("Utilization Pattern", "utilization_factor"),
        ("Useful Losses", "losses_useful"),
        ("Solar Gain", "gains_solar"),
        ("Internal Gains", "gains_internal"),
    ),
    "NBDM_PeakHeatingLoad": (
        ("Peak Heating Load", "peak_load"),
        ("Transmission Losses", "losses_transmission"),
        ("Ventilation Losses", "losses_ventilation"),
        ("Solar Gain", "gains_solar"),
        ("Internal Gains", "gains_internal"),
    ),
    "NBDM_PeakSensibleCoolingLoad": (
        ("Peak Cooling Load", "peak_load"),
        ("Transmission Losses", "losses_transmission"),
        ("Ventilation Losses", "losses_ventilation"),
        ("Solar Gain", "gains_solar"),
        ("Internal Gains", "gains_internal"),
    ),
}

bldg_segment_attributes = {
    "NBDM_BuildingSegment": (
        ("Segment Name", "segment_name"),
        ("Construction Type", "construction_type"),
        ("Construction Method", "construction_method"),
        ("Geometry", "geometry"),
        ("Occupancy", "occupancy"),
        ("Energy", "performance"),
    ),
    "NBDM_BuildingSegmentGeometry": (
        ("Envelope Area", "area_envelope"),
        ("Gross Floor Area", "area_floor_area_gross"),
        ("Net Interior Floor Area", "area_floor_area_net_interior_weighted"),
        ("Interior Parking Floor Area", "area_floor_area_interior_parking"),
        ("Gross Volume", "volume_gross"),
        ("Net Interior Volume", "volume_net_interior"),
        ("Num. Stories", "total_stories"),
        ("Num. Stories Above Grade", "num_stories_above_grade"),
        ("Num. Stories Below Grade", "num_stories_below_grade"),
    ),
    "NBDM_BuildingSegmentOccupancy": (
        ("Total Dwelling Units", "total_dwelling_units"),
        ("Num. Studio", "num_apartments_studio"),
        ("Num. 1Br", "num_apartments_1_br"),
        ("Num. 2Br", "num_apartments_2_br"),
        ("Num. 3Br", "num_apartments_3_br"),
        ("Num. 4Br", "num_apartments_4_br"),
        ("Total Num. Occupants", "total_occupants"),
    ),
    "NBDM_BuildingSegmentPerformance": (
        ("Annual Energy Cost (USD)", "energy_cost"),
        ("Annual Site (End) Energy", "site_energy"),
        ("Annual Source (Primary) Energy", "source_energy"),
        ("Annual Heating Demand", "annual_heating_energy_demand"),
        ("Annual Cooling Demand", "annual_cooling_energy_demand"),
        ("Peak Heating Load", "peak_heating_load"),
        ("Peak Cooling Load", "peak_sensible_cooling_load"),
    ),
    "NBDM_SiteEnergy": (
        ("Consumption: Gas", "consumption_gas"),
        ("Consumption: Electricity", "consumption_electricity"),
        ("Consumption: District Energy", "consumption_district_heat"),
        ("Consumption: Other", "consumption_other"),
        ("Production: Solar PV", "production_solar_photovoltaic"),
        ("Production Solar Thermal", "production_solar_thermal"),
        ("Production Other", "production_other"),
    ),
    "NBDM_SourceEnergy": (
        ("Consumption: Gas", "consumption_gas"),
        ("Consumption: Electricity", "consumption_electricity"),
        ("Consumption: District Energy", "consumption_district_heat"),
        ("Consumption: Other", "consumption_other"),
        ("Production: Solar PV", "production_solar_photovoltaic"),
        ("Production Solar Thermal", "production_solar_thermal"),
        ("Production Other", "production_other"),
    ),
    "NBDM_EnergyCost": (
        ("Cost: Gas", "cost_gas"),
        ("Cost: Electricity", "cost_electricity"),
        ("Cost: District Energy", "cost_district_heat"),
        ("Cost: Other", "cost_other_energy"),
    ),
    "NBDM_AnnualHeatingDemandEnergy": (
        ("Heating Demand", "annual_demand"),
        ("Transmission Losses", "losses_transmission"),
        ("Ventilation Losses", "losses_ventilation"),
        ("Solar Gain", "gains_solar"),
        ("Internal Gains", "gains_internal"),
        ("Utilization Pattern", "utilization_factor"),
        ("Useful Gains", "gains_useful"),
    ),
    "NBDM_AnnualCoolingDemandEnergy": (
        ("Cooling Demand", "annual_demand"),
        ("Transmission Losses", "losses_transmission"),
        ("Ventilation Losses", "losses_ventilation"),
        ("Utilization Pattern", "utilization_factor"),
        ("Useful Losses", "losses_useful"),
        ("Solar Gain", "gains_solar"),
        ("Internal Gains", "gains_internal"),
    ),
    "NBDM_PeakHeatingLoad": (
        ("Peak Heating Load", "peak_load"),
        ("Transmission Losses", "losses_transmission"),
        ("Ventilation Losses", "losses_ventilation"),
        ("Solar Gain", "gains_solar"),
        ("Internal Gains", "gains_internal"),
    ),
    "NBDM_PeakSensibleCoolingLoad": (
        ("Peak Cooling Load", "peak_load"),
        ("Transmission Losses", "losses_transmission"),
        ("Ventilation Losses", "losses_ventilation"),
        ("Solar Gain", "gains_solar"),
        ("Internal Gains", "gains_internal"),
    ),
}

# -----------------------------------------------------------------------------


@dataclass
class RowData:
    """Temp row-data class."""

    row_number: int
    display_name: Optional[str]
    value_baseline: Optional[Union[str, float, int]]
    value_proposed: Optional[Union[str, float, int]] = None
    value_change: Optional[Union[str, float, int]] = None
    level: int = 0
    range_color: Optional[Tuple[int, int, int]] = COLOR_BACKGROUND_DATA
    font_color: Tuple[int, int, int] = COLOR_FONT_DATA

    @classmethod
    def blank_line(cls, _row_number: int) -> "RowData":
        """Create a new blank row at the specified row-number."""
        return cls(_row_number, None, None)

    @classmethod
    def heading_1_line(
        cls,
        _row_number: int,
        _heading_display_name: Optional[str] = None,
        _heading_baseline: Optional[str] = None,
        _heading_proposed: Optional[str] = None,
        _heading_change: Optional[str] = None,
    ) -> "RowData":
        """Create a new 'header' row with a single name a the specified row-number.'"""
        row = cls(
            _row_number,
            _heading_display_name,
            _heading_baseline,
            _heading_proposed,
            _heading_change,
        )
        row.font_color = COLOR_FONT_HEADING_1
        row.range_color = COLOR_BACKGROUND_HEADING_1
        return row

    @classmethod
    def heading_2_line(
        cls,
        _row_number: int,
        _heading_display_name: Optional[str] = None,
        _heading_baseline: Optional[str] = None,
        _heading_proposed: Optional[str] = None,
        _heading_change: Optional[str] = None,
    ) -> "RowData":
        """Create a new 'header' row with a single name a the specified row-number.'"""
        row = cls(
            _row_number,
            _heading_display_name,
            _heading_baseline,
            _heading_proposed,
            _heading_change,
        )
        row.font_color = COLOR_FONT_HEADING_2
        row.range_color = COLOR_BACKGROUND_HEADING_2
        return row


def build_row_data(
    _baseline_obj,
    _proposed_obj,
    _change_obj,
    _start_row: int,
    _attr_dict: Dict[str, Tuple[Tuple[str, str]]],
) -> List[RowData]:
    """Return all the data from the NBDM Object Tree."""

    row_data = []

    def _get_attr(_obj, _attr_name: str):
        """Handle Enum .value when getting a field's value."""
        try:
            return getattr(_obj, _attr_name).value
        except AttributeError:
            return getattr(_obj, _attr_name, None)

    def _are_xl_writables(_baseline_obj, _proposed_obj, _change_obj):
        """Return True if all the input objects are XL-Writable"""
        xl_rng_val = (type(None), str, float, int)  # Can be written to XL directly

        if not isinstance(_baseline_obj, xl_rng_val):
            return False
        if not isinstance(_proposed_obj, xl_rng_val):
            return False
        if not isinstance(_change_obj, xl_rng_val):
            return False

        return True

    # -------------------------------------------------------------------------
    def walk_object(
        _baseline_obj, _proposed_obj, _change_obj, _start_row: int, _level: int
    ) -> Tuple[int, int]:
        """Walk through the Objects and get all their data, adding it to the 'row_data'."""

        row_num = _start_row
        level = _level  # Keep track of the indentation / hierarchy level

        # ---------------------------------------------------------------------
        # -- Get the Object's attribute report-order / display-names from the dict
        attribute_names = _attr_dict[_baseline_obj.__class__.__name__]

        for attr_display_name, attr_name in attribute_names:
            if attr_name.startswith("_"):
                continue

            # -----------------------------------------------------------------
            # -- Get the Attributes from each object
            attr_bsln = _get_attr(_baseline_obj, attr_name)
            attr_prpsd = _get_attr(_proposed_obj, attr_name)
            attr_change = _get_attr(_change_obj, attr_name)

            if _are_xl_writables(attr_bsln, attr_prpsd, attr_change):
                # -------------------------------------------------------------
                # -- The Attribute's value is writable to Excel directly (int, float, etc...)
                row_num += 1
                row_data.append(
                    RowData(
                        row_number=row_num,
                        display_name=attr_display_name,
                        value_baseline=attr_bsln,
                        value_proposed=attr_prpsd,
                        value_change=attr_change,
                        level=0,
                    )
                )
            else:
                # -------------------------------------------------------------
                # -- The Attribute's value is not writable to XL, it is an object with
                # -- fields of some sort, so walk through those and get all its attributes.

                # -- Add in a Blank break line
                row_num += 1
                row_data.append(RowData.blank_line(row_num))

                # -- Add in a Heading Line
                row_num += 1
                level += 1
                row_data.append(RowData.heading_1_line(row_num, attr_display_name))
                row_num, level = walk_object(
                    attr_bsln, attr_prpsd, attr_change, row_num, level
                )

        return row_num, level

    # -------------------------------------------------------------------------

    walk_object(_baseline_obj, _proposed_obj, _change_obj, _start_row, _level=0)

    return row_data


# -----------------------------------------------------------------------------


def Project(
    _sheet_name: str, _start_row: int, _p: project.NBDM_Project
) -> List[XlItem]:
    """Return the NBDM_Project's data as a list of XLItems."""

    # -- Add a Top-Level Heading row
    row_data_list = [RowData.heading_2_line(_start_row, "PROJECT")]
    _start_row += 1

    # -------------------------------------------------------------------------
    # -- Get all the row-data from the NBDM Objects
    row_data_list.extend(
        build_row_data(
            _baseline_obj=_p,
            _proposed_obj=None,
            _change_obj=None,
            _start_row=_start_row,
            _attr_dict=project_attributes,
        )
    )

    # -------------------------------------------------------------------------
    # -- Build the Excel items from all of the row-data collected
    xl_items = []
    for row_data in row_data_list:
        xl_items.append(
            XlItem(
                sheet_name=_sheet_name,
                xl_range=f"A{row_data.row_number}",
                write_value=[
                    row_data.display_name,
                    row_data.value_baseline,
                    row_data.value_proposed,
                    row_data.value_change,
                ],
                range_color=row_data.range_color,
                font_color=row_data.font_color,
            )
        )

    return xl_items


def Building(
    _sheet_name: str,
    _start_row: int,
    _bldg_baseline: building.NBDM_Building,
    _bldg_proposed: building.NBDM_Building,
    _bldg_change: building.NBDM_Building,
) -> List[XlItem]:
    """Return the NBDM_Building's data as a list of XLItems."""

    # -------------------------------------------------------------------------
    # -- Add a Blank Row
    row_data_list: List[RowData] = []
    row_data_list.append(RowData.blank_line(_start_row))
    _start_row += 1

    # -------------------------------------------------------------------------
    # -- Add a Top-Level Heading row
    heading = ("WHOLE BUILDING", "BASELINE", "PROPOSED", "CHANGE")
    row_data_list.append(RowData.heading_2_line(_start_row, *heading))
    _start_row += 1

    # -------------------------------------------------------------------------
    # -- Create the row data from the Objects
    object_row_data = build_row_data(
        _bldg_baseline, _bldg_proposed, _bldg_change, _start_row, bldg_attributes
    )
    row_data_list.extend(object_row_data)

    # -------------------------------------------------------------------------
    # -- Create XL-Items from the Row-Data
    xl_items = []
    for row_data in row_data_list:
        xl_items.append(
            XlItem(
                _sheet_name,
                f"A{row_data.row_number}",
                [
                    row_data.display_name,
                    row_data.value_baseline,
                    row_data.value_proposed,
                    row_data.value_change,
                ],
                range_color=row_data.range_color,
                font_color=row_data.font_color,
            )
        )
    return xl_items


def BuildingSegment(
    _sheet_name: str,
    _start_row: int,
    _bldg_seg_baseline: building.NBDM_BuildingSegment,
    _bldg_seg_proposed: building.NBDM_BuildingSegment,
    _bldg_seg_change: building.NBDM_BuildingSegment,
) -> List[XlItem]:
    """Return an NBDM_BuildingSegment's data as a List of XLItems."""

    # -------------------------------------------------------------------------
    # -- Add a Blank Row
    row_data_list: List[RowData] = []
    row_data_list.append(RowData.blank_line(_start_row))
    _start_row += 1

    # -------------------------------------------------------------------------
    # -- Add a Top-Level Heading row
    heading = ("BUILDING SEGMENT", "BASELINE", "PROPOSED", "CHANGE")
    row_data_list.append(RowData.heading_2_line(_start_row, *heading))
    _start_row += 1

    # -------------------------------------------------------------------------
    # -- Create the row data from the Objects
    object_row_data = build_row_data(
        _baseline_obj=_bldg_seg_baseline,
        _proposed_obj=_bldg_seg_proposed,
        _change_obj=_bldg_seg_change,
        _start_row=_start_row,
        _attr_dict=bldg_segment_attributes,
    )
    row_data_list.extend(object_row_data)

    # -------------------------------------------------------------------------
    # -- Create XL-Items from the Row-Data
    xl_items = []
    for row_data in row_data_list:
        xl_items.append(
            XlItem(
                sheet_name=_sheet_name,
                xl_range=f"A{row_data.row_number}",
                write_value=[
                    row_data.display_name,
                    row_data.value_baseline,
                    row_data.value_proposed,
                    row_data.value_change,
                ],
                range_color=row_data.range_color,
                font_color=row_data.font_color,
            )
        )

    return xl_items
