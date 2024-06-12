# -*- coding: utf-8 -*-
# -*- Python Version: 3.7 -*-

"""Operator functions (Add, Subtract) used by NBDM Objects."""

from __future__ import annotations

from dataclasses import fields
from typing import TypeVar

T = TypeVar("T")


def _check_types(_object_a: T, _object_b: T):
    """Raise Exception if the types of two NBDM Objects do not match."""
    if type(_object_a) != type(_object_b):
        msg = (
            f"\n\tError: Cannot operate on {_object_a} and {_object_b}."
            f"Different types: {type(_object_a)} / {type(_object_b)}"
        )
        raise Exception(msg)


def _check_field_names(_object_a: T, _object_b: T):
    """Raise Exception if the field-names of two NBDM Objects do not match."""
    if [f.name for f in fields(_object_a)] != [f.name for f in fields(_object_b)]:
        msg = f"\n\tError: Field names for object {_object_a} and object {_object_b} do not match?"
        raise Exception(msg)


def add_NBDM_Objects(_object_a: T, _object_b: T) -> T:
    """Add two NBDM Objects together."""

    _check_types(_object_a, _object_b)
    _check_field_names(_object_a, _object_b)

    new_attr_values = {}
    for field in fields(_object_a):
        try:
            val = getattr(_object_a, field.name) + getattr(_object_b, field.name)
            new_attr_values[field.name] = val
        except:
            new_attr_values[field.name] = None

    return _object_a.__class__(**new_attr_values)


def subtract_NBDM_Objects(_object_a: T, _object_b: T) -> T:
    """Subtract one NBDM Object from Another"""

    _check_types(_object_a, _object_b)
    _check_field_names(_object_a, _object_b)

    new_attr_values = {}
    for field in fields(_object_a):
        if field.type == str:
            new_attr_values[field.name] = getattr(_object_a, field.name)
        else:
            try:
                val = getattr(_object_a, field.name) - getattr(_object_b, field.name)
                new_attr_values[field.name] = val
            except:
                new_attr_values[field.name] = None

    return _object_a.__class__(**new_attr_values)
