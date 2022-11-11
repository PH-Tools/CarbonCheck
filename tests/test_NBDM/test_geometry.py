from dataclasses import asdict
from NBDM.model.geometry import NBDM_BuildingSegmentGeometry

def test_building_segment_geometry(sample_NBDM_BuildingSegmentGeometry):
    assert sample_NBDM_BuildingSegmentGeometry

def test_building_segment_geometry_to_dict(sample_NBDM_BuildingSegmentGeometry: NBDM_BuildingSegmentGeometry):
    d1 = asdict(sample_NBDM_BuildingSegmentGeometry)
    obj = NBDM_BuildingSegmentGeometry.from_dict(d1)
    d2 = asdict(obj)

    assert d1 == d2