# -*- coding: utf-8 -*-
# -*- Python Version: 3.7 -*-

"""Functions used for Serialization / Deserialization of NBDM Objects."""

from typing import Dict, Any


def build_attr_dict(_cls: Any, _d: Dict) -> Dict:
    """Create a Dict of NBDM objects based on an input Dict."""
    d = {}

    for attr_name in _cls.__dataclass_fields__.keys():

        attr_type = _cls.__dataclass_fields__[attr_name].type

        if hasattr(attr_type, "from_dict"):
            # -- if it is an object is a 'from_dict' method, call
            # -- that method and pass along the data dict
            d[attr_name] = attr_type.from_dict(_d[attr_name])
        else:
            # -- otherwise, just create a normal object
            d[attr_name] = attr_type(_d[attr_name])

    return d
