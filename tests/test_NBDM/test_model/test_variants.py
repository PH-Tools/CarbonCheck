from NBDM.model import serialization
from NBDM.model.project import NBDM_Project, NBDM_Variant, NBDM_Variants


def test_variants_to_dict(sample_NBDM_Project: NBDM_Project):
    d1 = serialization.to_dict(sample_NBDM_Project.variants)
    obj = NBDM_Variants.from_dict(d1)
    d2 = serialization.to_dict(obj)

    assert d1 == d2

    for variant in sample_NBDM_Project.variants:
        d1 = serialization.to_dict(variant)
        obj = NBDM_Variant.from_dict(d1)
        d2 = serialization.to_dict(obj)

    assert d1 == d2


def test_variants_bldg_seg_names(sample_NBDM_Project: NBDM_Project):
    proposed_names = sample_NBDM_Project.building_segment_names_proposed
    baseline_names = sample_NBDM_Project.building_segment_names_baseline

    assert proposed_names == baseline_names
    assert proposed_names is not None
    assert baseline_names is not None


def test_variants_bldg_segments_individual(sample_NBDM_Project: NBDM_Project):
    proposed_segments = sample_NBDM_Project.building_segments_proposed
    baseline_segments = sample_NBDM_Project.building_segments_baseline

    assert proposed_segments[0].segment_name == baseline_segments[0].segment_name


def test_variants_bldg_segments(sample_NBDM_Project: NBDM_Project):
    for seg_a, seg_b in sample_NBDM_Project.variants.building_segments:
        assert seg_a.segment_name == seg_b.segment_name


def test_change_from_baseline_variant(sample_NBDM_Project: NBDM_Project):
    baseline_var = sample_NBDM_Project.variants.baseline
    change_var = sample_NBDM_Project.variants.change_from_baseline_variant

    assert change_var.variant_name == baseline_var.variant_name
    assert len(change_var.building_segments) == len(baseline_var.building_segments)
    assert change_var.building_segment_names == baseline_var.building_segment_names
