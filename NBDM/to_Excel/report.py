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

            # -- Write out the Project site and data
            row_num = 0
            for xl_item in as_xl_items.Project(self.sheet_name, row_num, _nbdm_project):
                self.xl.write_xl_item(xl_item)
                row_num += 1

            # -- Write out the project's detailed building segment data
            for bldg_segment_name in _nbdm_project.building_segment_names:
                baseline_seg = _nbdm_project.variants.baseline.get_building_segment(
                    bldg_segment_name
                )
                proposed_seg = _nbdm_project.variants.proposed.get_building_segment(
                    bldg_segment_name
                )
                for xl_item in as_xl_items.BuildingSegment(
                    self.sheet_name, row_num, baseline_seg, proposed_seg
                ):
                    self.xl.write_xl_item(xl_item)
                    row_num += 1
