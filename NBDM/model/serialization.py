# -*- coding: utf-8 -*-
# -*- Python Version: 3.7 -*-

"""Functions used for Serialization / Deserialization of NBDM Objects."""

from typing import Dict, Any
from dataclasses import fields
from enum import Enum


class FromDictException(Exception):
    def __init__(self, _cls_name, _attr_name, _dict_keys):
        self.message = (
            f"\n\tError building{_cls_name} from dict."
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

    for field in fields(_cls):
        if field.name not in _d.keys():
            raise FromDictException(_cls.__name__, field.name, _d.keys())

        try:
            # -- If it is an object with a 'from_dict' method, call
            # -- the 'from_dict' method and pass along the data-dict
            d[field.name] = field.type.from_dict(_d[field.name])
        except AttributeError:
            # -- otherwise, just create a normal object
            try:
                d[field.name] = field.type(_d[field.name])
            except TypeError as e:
                msg = (
                    f"\n\tError: cannot use '{_d[field.name]}' for attribute "
                    f"'{field.name}'? Expected value of type: {field.type} ?\n"
                )
                raise TypeError(msg + str(e))

    return d


def to_dict(obj) -> Dict:
    """Recursively create a dictionary of the object's attribute values."""

    d = {}

    for field in fields(obj):
        field_value = getattr(obj, field.name)
        if hasattr(field_value, "__dataclass_fields__"):
            d[field.name] = to_dict(field_value)
        elif isinstance(field_value, (list, tuple)):
            d[field.name] = []
            for _ in field_value:
                d[field.name].append(to_dict(field_value))
        elif isinstance(field_value, dict):
            d[field.name] = {}
            for k, v in field_value.items():
                d[field.name][k] = to_dict(v)
        elif isinstance(field_value, Enum):
            d[field.name] = field_value.value
        else:
            d[field.name] = field_value

    return d
