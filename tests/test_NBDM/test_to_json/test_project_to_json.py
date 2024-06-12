import os
import pathlib

from NBDM.from_JSON.read import NBDM_Project_from_json_file
from NBDM.model.project import NBDM_Project
from NBDM.to_JSON.write import NBDM_Project_to_json_file


def test_write_project_to_json_file(sample_NBDM_Project: NBDM_Project) -> None:
    WRITE_FILE = pathlib.Path("__test_json_output_file__.json")
    try:
        NBDM_Project_to_json_file(sample_NBDM_Project, WRITE_FILE)
        assert pathlib.Path.exists(WRITE_FILE)
    finally:
        if pathlib.Path.exists(WRITE_FILE):
            os.remove(WRITE_FILE)


def test_write_project_to_json_file_then_read_back_in(
    sample_NBDM_Project: NBDM_Project,
) -> None:
    WRITE_FILE = pathlib.Path("__test_json_output_file__.json")
    try:
        NBDM_Project_to_json_file(sample_NBDM_Project, WRITE_FILE)
        new_project = NBDM_Project_from_json_file(WRITE_FILE)

        assert isinstance(new_project, NBDM_Project)
        assert new_project.project_name == sample_NBDM_Project.project_name
        assert new_project.team == sample_NBDM_Project.team
        assert new_project.site == sample_NBDM_Project.site

        # -- Check the Baseline Variants --------------------------------------
        baseline_a = new_project.variants.baseline.building
        baseline_b = sample_NBDM_Project.variants.baseline.building

        assert baseline_a.building_name == baseline_b.building_name
        assert baseline_a.building_segment_names == baseline_b.building_segment_names
        assert baseline_a.geometry == baseline_b.geometry
        assert baseline_a.occupancy == baseline_b.occupancy
        assert baseline_a.performance == baseline_b.performance

        # -- Check the Proposed Variants --------------------------------------
        proposed_a = new_project.variants.proposed.building
        proposed_b = sample_NBDM_Project.variants.proposed.building

        assert proposed_a.building_name == proposed_b.building_name
        assert proposed_a.building_segment_names == proposed_b.building_segment_names
        assert proposed_a.geometry == proposed_b.geometry
        assert proposed_a.occupancy == proposed_b.occupancy
        assert proposed_a.performance == proposed_b.performance

    finally:
        if pathlib.Path.exists(WRITE_FILE):
            os.remove(WRITE_FILE)
