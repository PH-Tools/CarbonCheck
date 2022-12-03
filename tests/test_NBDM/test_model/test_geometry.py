from dataclasses import asdict
from copy import copy
from NBDM.model.geometry import NBDM_BuildingSegmentGeometry


def test_building_segment_geometry(sample_NBDM_BuildingSegmentGeometry):
    assert sample_NBDM_BuildingSegmentGeometry


def test_building_segment_geometry_to_dict(
    sample_NBDM_BuildingSegmentGeometry: NBDM_BuildingSegmentGeometry,
):
    d1 = asdict(sample_NBDM_BuildingSegmentGeometry)
    obj = NBDM_BuildingSegmentGeometry.from_dict(d1)
    d2 = asdict(obj)

    assert d1 == d2


def test_subtract_segment_geometry(
    sample_NBDM_BuildingSegmentGeometry: NBDM_BuildingSegmentGeometry,
):
    g1 = copy(sample_NBDM_BuildingSegmentGeometry)
    g2 = copy(sample_NBDM_BuildingSegmentGeometry)
    g3 = g1 - g2

    assert g3.area_envelope == 0
    assert g3.area_floor_area_gross == 0
    assert g3.area_floor_area_net_interior_weighted == 0
    assert g3.area_floor_area_interior_parking == 0
    assert g3.volume_gross == 0
    assert g3.volume_net_interior == 0
    assert g3.total_stories == 0
    assert g3.num_stories_above_grade == 0
    assert g3.num_stories_below_grade == 0
