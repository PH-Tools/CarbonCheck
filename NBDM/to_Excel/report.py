# -*- coding: utf-8 -*-
# -*- Python Version: 3.7 -*-

"""Excel report generator / writer."""

from __future__ import annotations
from typing import Tuple
from copy import copy

from PHX.xl import xl_app, xl_typing

from NBDM.model.project import NBDM_Project
from NBDM.model.building import NBDM_BuildingSegment
from NBDM.to_Excel import as_xl_items


def group(start_offset: int, end_offset: int):
    """Decorator which 'Groups' the block when written to Excel."""

    def outer(write_function):
        def inner(*args, **kwargs):
            # -- Pull out the arguments
            report_obj: OutputReport = args[0]
            nbdm_project: NBDM_Project = args[1]
            row_num: int = args[2]

            # -- preserve the starting row num
            start_row: int = copy(row_num)
            group_start_row = start_row + start_offset

            # -- Execute the write to Excel function
            end_row_num: int = write_function(*args, **kwargs)

            group_end_row = end_row_num - end_offset

            # -- Group the rows written
            report_obj.xl.group_rows(
                report_obj.worksheet.name, group_start_row, group_end_row
            )

            return end_row_num

        return inner

    return outer


class OutputReport:
    """The Excel Output Report object with write-capability."""

    def __init__(self, _xl: xl_app.XLConnection, _sheet_name: str):
        self.xl = _xl
        self.worksheet = _sheet_name

    @property
    def worksheet(self) -> xl_typing.xl_Sheet_Protocol:
        """Return the Worksheet to write to."""
        return self._worksheet

    @worksheet.setter
    def worksheet(self, _sheet_name: str):
        """Set the write worksheet by name. Will create the worksheet if it does not exist."""
        self.xl.create_new_worksheet(_sheet_name)
        self._worksheet = self.xl.get_sheet_by_name(_sheet_name)

    def autofit_columns(self):
        self.xl.autofit_columns(self.worksheet.name)

    def hide_group_details(self):
        """Hide (collapse) all the 'Groups' on the Worksheet."""
        self.xl.hide_group_details(self.worksheet.name)

    @group(start_offset=10, end_offset=1)
    def write_NBDM_Project(self, _nbdm_project: NBDM_Project, row_num: int) -> int:
        """Write out a an NBDM Project's top-level data."""

        xl_items = as_xl_items.Project(self.worksheet.name, row_num, _nbdm_project)
        for xl_item in xl_items:
            self.xl.write_xl_item(xl_item)
            row_num += 1

        return row_num

    @group(start_offset=6, end_offset=1)
    def write_NBDM_WholeBuilding(self, _nbdm_project: NBDM_Project, row_num: int) -> int:
        """Write out the projects's whole-building data."""

        building = _nbdm_project.buildings_with_change
        # -- building: Tuple[baseline, proposed, change]
        xl_items = as_xl_items.Building(self.worksheet.name, row_num, *building)
        for xl_item in xl_items:
            self.xl.write_xl_item(xl_item)
            row_num += 1

        return row_num

    @group(start_offset=6, end_offset=1)
    def write_NBDM_BuildingSegment(
        self, _segment: Tuple[NBDM_BuildingSegment, ...], row_num: int
    ) -> int:
        """Write out a single BuildingSegment's data."""

        # -- _segment: Tuple[baseline, proposed, change]
        xl_items = as_xl_items.BuildingSegment(self.worksheet.name, row_num, *_segment)
        for xl_item in xl_items:
            self.xl.write_xl_item(xl_item)
            row_num += 1

        return row_num

    def write_NBDM_BuildingSegments(
        self, _nbdm_project: NBDM_Project, row_num: int
    ) -> int:
        """Write out each of the projects's BuildingSegment's data."""

        for segment in _nbdm_project.building_segments_with_change:
            # -- segment: Tuple[baseline, proposed, change]
            row_num = self.write_NBDM_BuildingSegment(segment, row_num)
        return row_num
