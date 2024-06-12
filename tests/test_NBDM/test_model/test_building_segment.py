from copy import copy

from NBDM.model import enums, serialization
from NBDM.model.building import NBDM_Building, NBDM_BuildingSegment


def test_building_segment_to_dict(sample_NBDM_Building: NBDM_Building):
    for seg in sample_NBDM_Building.building_segments:
        d1 = serialization.to_dict(seg)
        obj = NBDM_BuildingSegment.from_dict(d1)
        d2 = serialization.to_dict(obj)

        assert d1 == d2


def test_bldg_segment_alphabetical_order():
    sample_Building = NBDM_Building(
        building_name="A Sample Building",
        building_type=enums.building_type.MULTIFAMILY,
    )
    segment_names_in_alpha_order = sorted(
        [seg.segment_name for seg in sample_Building.building_segments]
    )
    assert sample_Building.building_segment_names == segment_names_in_alpha_order


def test_subtract_bldg_segments(sample_NBDM_Building: NBDM_Building):
    seg_1 = copy(sample_NBDM_Building.building_segments[0])
    seg_2 = copy(sample_NBDM_Building.building_segments[0])

    seg_3 = seg_1 - seg_2

    assert seg_3.segment_name == seg_1.segment_name
    assert seg_3.construction_type == seg_1.construction_type
    assert seg_3.construction_method == seg_1.construction_method
    assert seg_3.geometry == seg_1.geometry - seg_2.geometry
    assert seg_3.occupancy == seg_1.occupancy - seg_2.occupancy
    assert seg_3.performance == seg_1.performance - seg_2.performance
