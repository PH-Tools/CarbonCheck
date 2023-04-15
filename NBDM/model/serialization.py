# -*- coding: utf-8 -*-
# -*- Python Version: 3.7 -*-

"""Functions used for Serialization / Deserialization of NBDM Objects."""

from __future__ import annotations
from typing import Dict, Any, get_type_hints
from enum import Enum
from dataclasses import fields


class FromDictException(Exception):
    def __init__(self, _cls_name, _attr_name, _dict_keys):
        self.message = (
            f"\n\tError building '{_cls_name}' from dict."
            f"\n\tThe attribute '{_attr_name}' is missing from "
            f"in the dictionary keys: {_dict_keys} provided?"
        )
        super().__init__(self.message)


def build_attr_dict(_cls: Any, _d: Dict) -> Dict:
    """Return a Dict of NBDM objects based on an input Dict.

    This method is called during an NBDM object's 'from_dict' method and used
    to build up the object's attributes from a Dict.
    """
    d = {}

    # -- Note: can't just use dataclasses.fields(_cls) 'cus of
    # -- from __future__ import annotations breaks fields().
    for field_name, field_type in get_type_hints(_cls).items():
        if field_name not in _d.keys():
            raise FromDictException(_cls.__name__, field_name, _d.keys())
        try:
            # -- If it is an object with a 'from_dict' method, call
            # -- the 'from_dict' method and pass along the data-dict
            d[field_name] = field_type.from_dict(_d[field_name])
        except AttributeError:
            # -- otherwise, just create a normal object
            try:
                d[field_name] = field_type(_d[field_name])
            except TypeError as e:
                msg = (
                    f"\n\tError: cannot use '{_d[field_name]}' for attribute "
                    f"'{field_name}'? Expected value of type: {field_type} ?\n"
                )
                raise TypeError(msg + str(e))

    return d


def to_dict(obj) -> Dict:
    """Recursively create a dictionary of the object's attribute values."""

    d = {}

    # -- Note: can't just use dataclasses.fields(obj) 'cus of
    # -- from __future__ import annotations breaks fields.
    # for field_name, field_type in get_type_hints(obj).items():
    # -- wait.... now it IS working? WTF????
    for field in fields(obj):
        field_name = field.name
        field_type = field.type
        field_value = getattr(obj, field_name)
        if hasattr(field_value, "__dataclass_fields__"):
            d[field_name] = to_dict(field_value)
        elif isinstance(field_value, (list, tuple)):
            d[field_name] = []
            for _ in field_value:
                d[field_name].append(to_dict(field_value))
        elif isinstance(field_value, dict):
            d[field_name] = {}
            for k, v in field_value.items():
                d[field_name][k] = to_dict(v)
        elif isinstance(field_value, Enum):
            d[field_name] = field_value.value
        else:
            d[field_name] = field_value

    return d
