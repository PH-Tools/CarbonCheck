from copy import copy

import pytest

from NBDM.model import serialization
from NBDM.model.project import NBDM_Project, NBDM_Variant


def test_proposed_variant_to_dict(sample_NBDM_Project: NBDM_Project):
    d1 = serialization.to_dict(sample_NBDM_Project.variants.proposed)
    obj = NBDM_Variant.from_dict(d1)
    d2 = serialization.to_dict(obj)

    assert d1 == d2


def test_baseline_variant_to_dict(sample_NBDM_Project: NBDM_Project):
    d1 = serialization.to_dict(sample_NBDM_Project.variants.baseline)
    obj = NBDM_Variant.from_dict(d1)
    d2 = serialization.to_dict(obj)

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


def test_subtract_variants(sample_NBDM_Project: NBDM_Project):
    var_1 = copy(sample_NBDM_Project.variants.baseline)
    var_2 = copy(sample_NBDM_Project.variants.proposed)

    var_3 = var_1 - var_2

    assert var_3.variant_name == var_1.variant_name
    assert var_3.building_segment_names == var_1.building_segment_names
    assert len(var_3.building_segment_names) == len(var_1.building_segment_names)
