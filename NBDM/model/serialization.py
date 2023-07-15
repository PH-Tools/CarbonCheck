# -*- coding: utf-8 -*-
# -*- Python Version: 3.7 -*-

"""Functions used for Serialization / Deserialization of NBDM Objects."""

from __future__ import annotations

from typing import Dict, Any, get_type_hints
from enum import Enum
from uuid import UUID
from dataclasses import fields, is_dataclass

from NBDM.model.collections import Collection

from ph_units.unit_type import Unit


class FromDictException(Exception):
    def __init__(self, _cls_name, _attr_name, _dict_keys):
        self.message = (
            f"\n\tError building '{_cls_name}' from dict."
            f"\n\tThe attribute '{_attr_name}' is missing from "
            f"in the dictionary keys: {_dict_keys} provided?"
        )
        super().__init__(self.message)


def build_NBDM_obj_from_treeView(_cls: Any, _d: Dict) -> Any:
    """Return a Dict of NBDM objects based on an input Dict of treeView data.

    This method is called when building an NBDM object from a treeView.
    """
    d = {}

    # -- Note: can't just use dataclasses.fields(_cls) 'cus of
    # -- from __future__ import annotations breaks fields().
    for field_name, field_type in get_type_hints(_cls).items():
        if field_name not in _d.keys():
            raise FromDictException(_cls.__name__, field_name, _d.keys())

        val = _d[field_name]
        if isinstance(val, tuple) and field_type == Unit:
            # # -- It is a treeView tuple with the value and unit
            # -- clean up the value
            try:
                value = float(str(val.row_value).replace("-", "").replace(",", ""))
                d[field_name] = Unit(value, val.row_unit)
            except ValueError as e:
                msg = f"Error: the input value for '{field_name}' of '{val.row_value}' is not valid. Only numbers are allowed."
                print("- " * 45)
                print(msg)
                print(e)
                print("- " * 45)
        elif is_dataclass(field_type) and isinstance(val, Dict):
            # -- Its another NBDM object that needs to be built.
            d[field_name] = build_NBDM_obj_from_treeView(field_type, val)
        else:
            # -- It is a regular str, float, int value
            try:
                d[field_name] = field_type(val.row_value)
            except Exception as e:
                msg = f"Error setting the attribute '{_cls.__name__}.{field_name}' to '{val.row_value}'"
                print("- " * 45)
                print(msg)
                print(e)
                print("- " * 45)

    return _cls(**d)


def build_NBDM_obj_from_dict(_cls: Any, _d: Dict) -> Any:
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

        field_data = _d[field_name]
        if field_type == Unit:
            d[field_name] = Unit.from_dict(field_data)
        elif hasattr(field_type, "from_dict"):
            d[field_name] = field_type.from_dict(field_data)
        else:
            d[field_name] = field_type(field_data)

    return _cls(**d)


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

        # ------------------------------------------------------------
        # -- A Collection object. Call to_dict() on it.
        if isinstance(field_value, Collection):
            _d = {}
            for collection_item in field_value:
                _d[collection_item.key] = to_dict(collection_item)
            d[field_name] = _d

        # ------------------------------------------------------------
        # -- A Dataclass / NBM Object. Just call to_dict() on it.
        elif hasattr(field_value, "__dataclass_fields__"):
            d[field_name] = to_dict(field_value)

        # ------------------------------------------------------------
        # -- A list of objects, call to_dict() on each one.
        elif isinstance(field_value, (list, tuple)):
            d[field_name] = []
            for _ in field_value:
                d[field_name].append(to_dict(field_value))

        # ------------------------------------------------------------
        # -- A dict object, call to_dict() on each value in the dict
        elif isinstance(field_value, dict):
            d[field_name] = {}
            for k, v in field_value.items():
                d[field_name][k] = to_dict(v)

        # ------------------------------------------------------------
        # -- An Enum object, just get the value of it.
        elif isinstance(field_value, Enum):
            d[field_name] = field_value.value

        # ------------------------------------------------------------
        # -- A Unit object with a value, call to_dict() on it.
        elif isinstance(field_value, Unit):
            d[field_name] = field_value.to_dict()

        # ------------------------------------------------------------
        # -- A UUID, just convert it to a string.
        elif isinstance(field_value, UUID):
            d[field_name] = str(field_value)

        else:
            d[field_name] = field_value

    return d
