from dataclasses import asdict
import pytest
from NBDM.model.project import NBDM_Project, NBDM_Variant


def test_proposed_variant_to_dict(sample_NBDM_Project: NBDM_Project):
    d1 = asdict(sample_NBDM_Project.variants.proposed)
    obj = NBDM_Variant.from_dict(d1)
    d2 = asdict(obj)

    assert d1 == d2


def test_baseline_variant_to_dict(sample_NBDM_Project: NBDM_Project):
    d1 = asdict(sample_NBDM_Project.variants.baseline)
    obj = NBDM_Variant.from_dict(d1)
    d2 = asdict(obj)

    assert d1 == d2


def test_variant_get_bldg_segment_names(sample_NBDM_Project: NBDM_Project):
    # -- Get a valid Segment
    seg_name = sample_NBDM_Project.building_segment_names_baseline[0]
    assert seg_name is not None


def test_variant_get_valid_bldg_segment(sample_NBDM_Project: NBDM_Project):
    # -- Get a valid Segment
    seg_name = sample_NBDM_Project.building_segment_names_baseline[0]
    seg = sample_NBDM_Project.variants.baseline.get_building_segment(seg_name)
    assert seg is not None


def test_variant_get_missing_bldg_segment(sample_NBDM_Project: NBDM_Project):
    with pytest.raises(KeyError):
        sample_NBDM_Project.variants.baseline.get_building_segment("Not A Name")


def test_variant_building_segments(sample_NBDM_Project: NBDM_Project):
    segments = sample_NBDM_Project.variants.baseline.building_segments
    assert segments is not None
    assert len(segments) == len(
        sample_NBDM_Project.variants.baseline.building_segment_names
    )
