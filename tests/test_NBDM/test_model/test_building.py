from dataclasses import asdict
from copy import copy
from NBDM.model.building import NBDM_Building
from NBDM.model import serialization


def test_building(sample_NBDM_Building):
    assert sample_NBDM_Building


def test_building_to_dict(sample_NBDM_Building: NBDM_Building):
    d1 = serialization.to_dict(sample_NBDM_Building)
    obj = NBDM_Building.from_dict(d1)
    d2 = serialization.to_dict(obj)

    assert d1 == d2
    assert len(sample_NBDM_Building.building_segments) == len(obj.building_segments)


def test_subtract_buildings(sample_NBDM_Building: NBDM_Building):
    b1 = copy(sample_NBDM_Building)
    b2 = copy(sample_NBDM_Building)

    b3 = b1 - b2

    assert b3.building_name == b1.building_name
    assert b3.building_type == b1.building_type
    assert len(b3.building_segments) == len(b1.building_segments)
    assert len(b3.building_segment_names) == len(b1.building_segment_names)
