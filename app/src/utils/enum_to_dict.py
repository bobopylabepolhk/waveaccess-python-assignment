from enum import Enum


def enum_to_dict(e: Enum):
    return {i.name: i.value for i in e}
