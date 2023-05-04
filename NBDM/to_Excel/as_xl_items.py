# -*- coding: utf-8 -*-
# -*- Python Version: 3.7 -*-

"""Functions to convert NBDM Project/Building/Segment objects into Excel Report writable items."""

from dataclasses import dataclass
from typing import Optional, List, Union, Tuple

from PHX.xl import xl_data
from NBDM.to_Excel import report_styles
from NBDM.model import output_format, project, building


@dataclass
class RowData:
    """Temp row-data class."""

    row_number: int
    display_name: Optional[str]
    value_baseline: Optional[Union[str, float, int]]
    value_proposed: Optional[Union[str, float, int]] = None
    value_change: Optional[Union[str, float, int]] = None
    level: int = 0
    range_color: Optional[Tuple[int, int, int]] = report_styles.COLOR_BACKGROUND_DATA
    font_color: Tuple[int, int, int] = report_styles.COLOR_FONT_DATA

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
        row.font_color = report_styles.COLOR_FONT_HEADING_1
        row.range_color = report_styles.COLOR_BACKGROUND_HEADING_1
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
        row.font_color = report_styles.COLOR_FONT_HEADING_2
        row.range_color = report_styles.COLOR_BACKGROUND_HEADING_2
        return row


def build_row_data(
    _baseline_obj,
    _proposed_obj,
    _change_obj,
    _start_row: int,
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

    def _get_object_format(_object):
        return getattr(output_format, f"Format_{_object.__class__.__name__}")

    # -------------------------------------------------------------------------
    def walk_object(
        _baseline_obj, _proposed_obj, _change_obj, _start_row: int, _level: int
    ) -> Tuple[int, int]:
        """Walk through the Objects and get all their data, adding it to the 'row_data'."""

        row_num = _start_row
        level = _level  # Keep track of the indentation / hierarchy level

        # ---------------------------------------------------------------------
        # -- Get the Object's attribute report-order / display-names from the dict
        object_format = _get_object_format(_baseline_obj)
        for attr_name, attr_display_name in vars(object_format).items():
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
# -- NBDM Class converters


def Project(
    _sheet_name: str, _start_row: int, _p: project.NBDM_Project
) -> List[xl_data.XlItem]:
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
        )
    )

    # -------------------------------------------------------------------------
    # -- Build the Excel items from all of the row-data collected
    xl_items = []
    for row_data in row_data_list:
        xl_items.append(
            xl_data.XlItem(
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
) -> List[xl_data.XlItem]:
    """Return the NBDM_Building's data as a list of XLItems."""

    row_data_list: List[RowData] = []

    # -------------------------------------------------------------------------
    # -- Add a Top-Level Heading row
    heading = ("WHOLE BUILDING", "BASELINE", "PROPOSED", "CHANGE")
    row_data_list.append(RowData.heading_2_line(_start_row, *heading))
    _start_row += 1

    # -------------------------------------------------------------------------
    # -- Create the row data from the Objects
    object_row_data = build_row_data(
        _bldg_baseline,
        _bldg_proposed,
        _bldg_change,
        _start_row,
    )
    row_data_list.extend(object_row_data)

    # -------------------------------------------------------------------------
    # -- Create XL-Items from the Row-Data
    xl_items = []
    for row_data in row_data_list:
        xl_items.append(
            xl_data.XlItem(
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
) -> List[xl_data.XlItem]:
    """Return an NBDM_BuildingSegment's data as a List of XLItems."""

    row_data_list: List[RowData] = []

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
    )
    row_data_list.extend(object_row_data)

    # -------------------------------------------------------------------------
    # -- Create XL-Items from the Row-Data
    xl_items = []
    for row_data in row_data_list:
        xl_items.append(
            xl_data.XlItem(
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


def Log(_sheet_name: str, _start_row: int, _log_data: List[str]) -> xl_data.XLItem_List:
    def _include_data(row: str) -> bool:
        if row.startswith("Reading:"):
            return False
        return True
    
    return xl_data.XLItem_List(
        [
            xl_data.XlItem(sheet_name=_sheet_name, xl_range=f"A{_start_row}", write_value=row,) 
            for row in _log_data if _include_data(row)
        ]
    )

