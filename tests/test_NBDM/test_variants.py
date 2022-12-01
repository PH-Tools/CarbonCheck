from dataclasses import asdict
import pytest
from NBDM.model.project import NBDM_Project, NBDM_Variants, NBDM_Variant


def test_variants_to_dict(sample_NBDM_Project: NBDM_Project):
    d1 = asdict(sample_NBDM_Project.variants)
    obj = NBDM_Variants.from_dict(d1)
    d2 = asdict(obj)

    assert d1 == d2

    for variant in sample_NBDM_Project.variants:
        d1 = asdict(variant)
        obj = NBDM_Variant.from_dict(d1)
        d2 = asdict(obj)

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
