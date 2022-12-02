# -*- coding: utf-8 -*-
# -*- Python Version: 3.7 -*-

"""Excel report generator / writer."""

from NBDM.to_Excel import xl_app
from NBDM.model import project
from NBDM.to_Excel import as_xl_items


class OutputReport:
    def __init__(self, _xl: xl_app.XLConnection):

        # -- Setup the Excel connection and facade object
        self.xl = _xl
        self.sheet_name = "NBDM"

    def write_NBDM_Project(self, _nbdm_project: project.NBDM_Project) -> None:
        """Write out a an NBDM Project to an Excel Worksheet."""

        if not self.xl.connection_is_open():
            raise xl_app.NoActiveExcelRunningError()

        with self.xl.in_silent_mode():
            self.xl.create_new_worksheet(self.sheet_name)

            # -- 1) Write out the Project site and data
            row_num = 0
            for xl_item in as_xl_items.Project(self.sheet_name, row_num, _nbdm_project):
                self.xl.write_xl_item(xl_item)
                row_num += 1

            # -- 2) Write out the projects's whole-building data
            baseline_bldg, proposed_bldg = _nbdm_project.buildings
            for xl_item in as_xl_items.Building(
                self.sheet_name, row_num, baseline_bldg, proposed_bldg
            ):
                self.xl.write_xl_item(xl_item)
                row_num += 1

            # -- 3) Write out the project's detailed building-segment data
            for baseline_seg, proposed_seg in _nbdm_project.building_segments:
                for xl_item in as_xl_items.BuildingSegment(
                    self.sheet_name, row_num, baseline_seg, proposed_seg
                ):
                    self.xl.write_xl_item(xl_item)
                    row_num += 1
