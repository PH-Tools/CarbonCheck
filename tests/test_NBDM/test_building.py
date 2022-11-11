from dataclasses import asdict
from NBDM.model.building import NBDM_Building, NBDM_BuildingSegment

def test_building(sample_NBDM_Building):
    assert sample_NBDM_Building

def test_building_to_dict(sample_NBDM_Building: NBDM_Building):
    d1 = asdict(sample_NBDM_Building)
    obj = NBDM_Building.from_dict(d1)
    d2 = asdict(obj)

    assert d1 == d2
    assert len(sample_NBDM_Building.building_segments) == len(obj.building_segments)

def test_building_segment_to_dict(sample_NBDM_Building: NBDM_Building):
    for seg in sample_NBDM_Building.building_segments:
        d1 = asdict(seg)
        obj = NBDM_BuildingSegment.from_dict(d1)
        d2 = asdict(obj)

        assert d1 == d2
