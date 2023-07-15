from NBDM.model.project import NBDM_Project
from NBDM.model import serialization


def test_project(sample_NBDM_Project: NBDM_Project):
    assert sample_NBDM_Project


def test_project_to_dict(sample_NBDM_Project: NBDM_Project):
    d1 = serialization.to_dict(sample_NBDM_Project)
    obj = NBDM_Project.from_dict(d1)
    d2 = serialization.to_dict(obj)

    assert d1 == d2


def test_project_bldg_segments(sample_NBDM_Project: NBDM_Project):
    for seg_a, seg_b in sample_NBDM_Project.building_segments:
        assert seg_a.segment_name == seg_b.segment_name
