from copy import copy

from ph_units.unit_type import Unit

from NBDM.model import serialization
from NBDM.model.geometry import NBDM_BuildingSegmentGeometry


def test_building_segment_geometry(sample_NBDM_BuildingSegmentGeometry):
    assert sample_NBDM_BuildingSegmentGeometry


def test_building_segment_geometry_to_dict(
    sample_NBDM_BuildingSegmentGeometry: NBDM_BuildingSegmentGeometry,
):
    d1 = serialization.to_dict(sample_NBDM_BuildingSegmentGeometry)
    obj = NBDM_BuildingSegmentGeometry.from_dict(d1)
    d2 = serialization.to_dict(obj)

    assert d1 == d2


def test_subtract_segment_geometry(
    sample_NBDM_BuildingSegmentGeometry: NBDM_BuildingSegmentGeometry,
):
    g1 = copy(sample_NBDM_BuildingSegmentGeometry)
    g2 = copy(sample_NBDM_BuildingSegmentGeometry)
    g3 = g1 - g2

    assert g3.area_envelope == Unit(0.0, "M2")
    assert g3.area_floor_area_net_interior_weighted == Unit(0.0, "M2")
    assert g3.volume_net_interior == Unit(0.0, "M2")
