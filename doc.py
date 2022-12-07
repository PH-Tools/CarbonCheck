"""Function to output a text description of the Model class hierarchy."""
from dataclasses import fields
from typing import List, Dict, Optional
import enum

from NBDM.model import project, building


def is_dict_field(_type: type) -> bool:
    if getattr(_type, "__origin__", None) == dict:
        return True
    return False


def is_dataclass_type(_type: type) -> bool:
    if not hasattr(_type, "__dataclass_fields__"):
        return False
    return True


def is_NBDM_class(_type: type) -> bool:
    if not is_dataclass_type(_type):
        return False
    if "NBDM" not in _type.__name__.upper():
        return False
    return True


def is_enum(_type: type) -> bool:
    return issubclass(_type, enum.Enum)


def build_txt(_type: type, _txt: List[str], _level: int) -> List[str]:
    for f in fields(_type):

        if is_dict_field(f.type):
            padding = "  " * _level
            _txt.append(f"{padding}{f.name} <{f.type}>")
            # TODO: walk through?
        elif is_NBDM_class(f.type):
            padding = "  " * _level
            padding = padding + "+"
            _txt.append(f"{padding}{f.name} <{f.type.__name__}>")
            underline = "-" * (79 - len(padding))
            _txt.append(f"{underline: >79}")
            _ = []
            build_txt(f.type, _, _level + 1)
            _txt.extend(_)
        else:
            padding = "  " * _level
            _txt.append(f"{padding}{f.name} <{f.type.__name__}>")

    return _txt


def build_mermaid(_type: type, _txt: List[str], _parent: type) -> List[str]:

    # -- Build the class attribute list
    txt.append(f"class {_type.__name__}{{")
    for f in fields(_type):
        if is_dict_field(f.type):
            return []
        line = f"{f.name}: {f.type.__name__}"
        _txt.append(line)
    _txt.append("}")

    # -- Build any Enums
    for f in fields(_type):
        if is_enum(f.type):
            _txt.append(f"class {f.name}{{")
            for field in dir(f.type):
                if not field.startswith("__"):
                    _txt.append(f"{f.name} : {field}")
                    getattr(f.type, field)
            _txt.append("}")
            _txt.append(f"{_parent.__name__} <-- {f.name}")

    # -- Build any NBDM Objects
    for f in fields(_type):
        if is_dict_field(f.type):
            continue
        elif is_NBDM_class(f.type):
            build_mermaid(f.type, _txt, _type)
            _txt.append(f"{_parent.__name__} <-- {f.name}")

    return _txt


txt = ["```mermaid"]
txt.append("classDiagram")
txt = build_mermaid(project.NBDM_Project, txt, project.NBDM_Project)
txt.append("```")

with open("testing.md", "w") as f:
    for l in txt:
        f.write(l)
        f.write("\n")
