from typing import Any, TypedDict, Union


class Value(TypedDict):
    name: str
    old: Union[str, bool]
    new: Union[str, bool]
    owner: "Component"
    type: str


class Options(TypedDict):
    name: str
    old: tuple[str, ...]
    new: tuple[Any, ...]
    owner: "Component"
    type: str


ChangeTypes = Union[Value, Options]
