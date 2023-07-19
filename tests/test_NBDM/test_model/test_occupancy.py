from dataclasses import asdict
from NBDM.model.occupancy import NBDM_BuildingSegmentOccupancy


def test_building_segment_occupancy(sample_NBDM_BuildingSegmentOccupancy) -> None:
    assert sample_NBDM_BuildingSegmentOccupancy


def test_building_segment_geometry_to_dict(
    sample_NBDM_BuildingSegmentOccupancy: NBDM_BuildingSegmentOccupancy,
) -> None:
    d1 = asdict(sample_NBDM_BuildingSegmentOccupancy)
    obj = NBDM_BuildingSegmentOccupancy.from_dict(d1)
    d2 = asdict(obj)

    assert d1 == d2
