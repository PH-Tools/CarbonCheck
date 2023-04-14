# -*- coding: utf-8 -*-
# -*- Python Version: 3.7 -*-

"""Excel report generator / writer."""

from __future__ import annotations
from copy import copy
from typing import Tuple
import inspect

from PHX.xl import xl_app

from NBDM.model.project import NBDM_Project
from NBDM.model.building import NBDM_BuildingSegment
from NBDM.to_Excel import as_xl_items

row_num = int  # type alias


def group(start_offset: int, end_offset: int):
    """Decorator which 'Groups' the block when written to Excel."""

    def outer(write_function):
        sig = inspect.signature(write_function)

        def inner(*args, **kwargs):
            # -- Use 'bind' to pull out all the arguments, (args, kwargs, etc...)
            # -- and combine them together into a single OrderedDict.
            # -- https://stackoverflow.com/questions/31728346/passing-default-arguments-to-a-decorator-in-python
            bound = sig.bind(*args, **kwargs)
            bound.apply_defaults()

            print(bound.arguments.keys())

            # -- Pull out the arguments
            report_obj: OutputReport = bound.arguments["self"]
            nbdm_project: NBDM_Project = bound.arguments["_nbdm_object"]
            row_num: int = bound.arguments["_row_num"]
            worksheet_name: str = bound.arguments["_worksheet_name"]

            # -- preserve the starting row num
            start_row: int = copy(row_num)
            group_start_row = start_row + start_offset

            # -- Execute the write to Excel function
            end_row_num: int = write_function(*args, **kwargs)

            group_end_row = end_row_num - end_offset

            # -- Group the rows written
            report_obj.xl.group_rows(worksheet_name, group_start_row, group_end_row)

            return end_row_num

        return inner

    return outer


class OutputReport:
    """The Excel Output Report object with write-capability."""

    def __init__(self, _xl: xl_app.XLConnection, _autofit: bool, _hide_groups: bool):
        self.xl = _xl
        self.autofit = _autofit
        self.hide_groups = _hide_groups

    def get_worksheet(self, _worksheet_name: str) -> xl_app.xl_Sheet_Protocol:
        """Return a Worksheet from the Workbook by name."""
        if _worksheet_name not in self.xl.get_worksheet_names():
            last_sheet_name = self.xl.get_last_sheet().name
            self.xl.create_new_worksheet(_worksheet_name, after=last_sheet_name)
        return self.xl.get_sheet_by_name(_worksheet_name)

    def autofit_columns(self, _worksheet_name: str) -> None:
        """Autofit (widen) the columns to fit the data on the specified Worksheet."""
        if self.autofit:
            self.xl.autofit_columns(_worksheet_name)

    def hide_group_details(self, _worksheet_name: str) -> None:
        """Hide (collapse) all the 'Groups' on the specified Worksheet."""
        if self.hide_groups:
            self.xl.hide_group_details(_worksheet_name)

    @group(start_offset=10, end_offset=1)
    def write_NBDM_Project(
        self,
        *,
        _nbdm_object: NBDM_Project,
        _row_num: int = 1,
        _worksheet_name: str = "Project Data",
    ) -> row_num:
        """Write out a an NBDM Project's top-level data."""
        worksheet = self.get_worksheet(_worksheet_name)
        xl_items = as_xl_items.Project(worksheet.name, _row_num, _nbdm_object)
        for xl_item in xl_items:
            self.xl.write_xl_item(xl_item)
            _row_num += 1

        self.autofit_columns(worksheet.name)
        self.hide_group_details(_worksheet_name)

        return _row_num

    @group(start_offset=6, end_offset=1)
    def write_NBDM_WholeBuilding(
        self,
        *,
        _nbdm_object: NBDM_Project,
        _row_num: int = 1,
        _worksheet_name: str = "Building Data",
    ) -> row_num:
        """Write out the projects's whole-building data."""

        building = _nbdm_object.buildings_with_change
        # -- building: Tuple[baseline, proposed, change]
        worksheet = self.get_worksheet(_worksheet_name)
        xl_items = as_xl_items.Building(worksheet.name, _row_num, *building)
        for xl_item in xl_items:
            self.xl.write_xl_item(xl_item)
            _row_num += 1

        self.autofit_columns(worksheet.name)
        self.hide_group_details(_worksheet_name)

        return _row_num

    @group(start_offset=6, end_offset=1)
    def write_NBDM_BuildingSegment(
        self,
        *,
        _nbdm_object: Tuple[NBDM_BuildingSegment, ...],
        _row_num: int = 1,
        _worksheet_name: str = "",
    ) -> row_num:
        """Write out a single BuildingSegment's data."""

        # -- _segment: Tuple[baseline, proposed, change]
        worksheet = self.get_worksheet(_worksheet_name)
        xl_items = as_xl_items.BuildingSegment(worksheet.name, _row_num, *_nbdm_object)
        for xl_item in xl_items:
            self.xl.write_xl_item(xl_item)
            _row_num += 1

        self.autofit_columns(worksheet.name)
        self.hide_group_details(_worksheet_name)

        return _row_num

    def write_NBDM_BuildingSegments(
        self, *, _nbdm_object: NBDM_Project, _row_num: int = 1
    ) -> row_num:
        """Write out each of the projects's BuildingSegment's data."""

        for segment in _nbdm_object.building_segments_with_change:
            # -- segment: Tuple[baseline, proposed, change]
            worksheet = self.get_worksheet(segment[0].segment_name)
            self.write_NBDM_BuildingSegment(
                _nbdm_object=segment, _row_num=_row_num, _worksheet_name=worksheet.name
            )
        return _row_num

    def remove_sheet_1(self) -> None:
        """Remove the default "Sheet1" from the workbook."""
        sheet_name = "Sheet1"
        try:
            sheet1 = self.xl.get_sheet_by_name("Sheet1")
            sheet1.delete()
        except KeyError:
            return None
