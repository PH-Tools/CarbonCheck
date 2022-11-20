# -*- coding: utf-8 -*-
# -*- Python Version: 3.7 -*-

"""Schemas to convert NBDM Objects into Excel Report writable items."""

from dataclasses import dataclass
from typing import Optional, List, Union, Dict, Tuple

from NBDM.model import project, building
from NBDM.to_Excel.xl_data import XlItem

COLOR_BACKGROUND_DATA = None
COLOR_BACKGROUND_HEADING = (100, 100, 100)
COLOR_BACKGROUND_LEVEL_1 = (220, 220, 220)
COLOR_FONT_HEADING = (255, 255, 255)

project_attributes = {
    "NBDM_Project": (
        ("Project Name", "project_name"),
        ("Client", "client"),
        ("Site", "site"),
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

bldg_segment_attributes = {
    "NBDM_BuildingSegment": (
        ("Segment Name", "segment_name"),
        ("Geometry", "geometry"),
        ("Occupancy", "occupancy"),
        ("Energy", "performance"),
    ),
    "NBDM_BuildingSegmentGeometry": (
        ("Envelope Area", "area_envelope:"),
        ("Gross Floor Area", "area_floor_area_gross:"),
        ("Net Interior Floor Area", "area_floor_area_net_interior_weighted:"),
        ("Interior Parking Floor Area", "area_floor_area_interior_parking:"),
        ("Gross Volume", "volume_gross:"),
        ("Net Interior Volume", "volume_net_interior:"),
        ("Num. Stories", "total_stories:"),
        ("Num. Stories Above Grade", "num_stories_above_grade:"),
        ("Num. Stories Below Grade", "num_stories_below_grade:"),
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
        ("Site (End) Energy", "site_energy"),
        ("Source (Primary) Energy", "source_energy"),
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


@dataclass
class RowData:
    """Temp row-data class."""

    row_number: int
    display_name: Optional[str]
    value_baseline: Optional[Union[str, float, int]]
    value_proposed: Optional[Union[str, float, int]] = None
    level: int = 0

    @property
    def range_color(self) -> Optional[Tuple[int, ...]]:
        """Make the Cell grey if its a 'heading' level row."""

        if self.level == 0:
            return COLOR_BACKGROUND_DATA
        else:
            return COLOR_BACKGROUND_LEVEL_1


def build_row_data(
    _baseline_obj,
    _proposed_obj,
    _start_row: int,
    _attr_dict: Dict[str, Tuple[Tuple[str, str]]],
) -> List[RowData]:
    """Return all the data from the NBDM Object Tree."""

    row_data = []
    xl_range_value = (type(None), str, float, int)  # Can be written to XL

    def walk_object(
        _baseline_obj, _proposed_obj, _start_row: int, _level: int
    ) -> Tuple[int, int]:
        """Walk through the Objects and get all their data, adding it to the 'row_data'."""

        row_num = _start_row
        level = _level  # Keep track of the indentation / hierarchy level

        attrs = _attr_dict[_baseline_obj.__class__.__name__]
        for attr_display_name, attr_name in attrs:
            if attr_name.startswith("_"):
                continue

            attr_baseline = getattr(_baseline_obj, attr_name, None)
            attr_proposed = getattr(_proposed_obj, attr_name, None)

            if isinstance(attr_baseline, xl_range_value):
                row_num += 1
                row_data.append(
                    RowData(row_num, attr_display_name, attr_baseline, attr_proposed, 0)
                )
            else:
                # -- Add in a Blank break line
                row_num += 1
                row_data.append(RowData(row_num, None, None, None))

                # -- Add in a Heading Line
                row_num += 1
                level += 1
                row_data.append(RowData(row_num, attr_display_name, None, None, level))
                row_num, level = walk_object(
                    attr_baseline, attr_proposed, row_num, level
                )

        return row_num, level

    walk_object(_baseline_obj, _proposed_obj, _start_row, _level=0)

    return row_data


# -----------------------------------------------------------------------------


def Project(
    _sheet_name: str, _start_row: int, _p: project.NBDM_Project
) -> List[XlItem]:
    """Return the NBDM Project's data as a list of XLItems."""

    xl_items = []
    # -- Add a Heading / Break line
    _start_row += 1
    xl_items.append(
        XlItem(
            _sheet_name,
            f"A{_start_row}",
            [None, "BASELINE", "PROPOSED"],
            range_color=COLOR_BACKGROUND_HEADING,
            font_color=COLOR_FONT_HEADING,
        )
    )
    _start_row += 1

    # -- Get the row-data from the NBDM Objects
    row_data_list = build_row_data(_p, _p, _start_row, project_attributes)

    # -- Build the Excel items from the row-data
    for row_data in row_data_list:
        xl_items.append(
            XlItem(
                _sheet_name,
                f"A{row_data.row_number}",
                [
                    row_data.display_name,
                    row_data.value_baseline,
                    row_data.value_proposed,
                ],
                range_color=row_data.range_color,
            )
        )

    return xl_items


def BuildingSegment(
    _sheet_name: str,
    _start_row: int,
    _s_baseline: building.NBDM_BuildingSegment,
    _s_proposed: building.NBDM_BuildingSegment,
) -> List[XlItem]:
    """Return an NBDM Building Segment's data as a List of XLItems."""
    xl_items = []
    # -- Add a Heading / Break line
    _start_row += 1
    xl_items.append(
        XlItem(
            _sheet_name,
            f"A{_start_row}",
            [None, None, None],
            range_color=COLOR_BACKGROUND_DATA,
        )
    )
    _start_row += 1
    xl_items.append(
        XlItem(
            _sheet_name,
            f"A{_start_row}",
            ["BUILDING SEGMENT", None, None],
            range_color=COLOR_BACKGROUND_HEADING,
            font_color=COLOR_FONT_HEADING,
        )
    )

    # -- Create the row data from the Objects
    row_data_list = build_row_data(
        _s_baseline, _s_proposed, _start_row, bldg_segment_attributes
    )

    # -- Crate XL-Items from the Row-Data
    for row_data in row_data_list:
        xl_items.append(
            XlItem(
                _sheet_name,
                f"A{row_data.row_number}",
                [
                    row_data.display_name,
                    row_data.value_baseline,
                    row_data.value_proposed,
                ],
                range_color=row_data.range_color,
            )
        )

    return xl_items
