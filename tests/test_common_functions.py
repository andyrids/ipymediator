# pyright: reportGeneralTypeIssues=false, reportAttributeAccessIssue=false
import pathlib
from typing import Union
from ipymediator.enumerations import Value, IconUnicode
from ipymediator.interface import Component, Mediator
from ipymediator.utils import (
    directory_contents,
    directory_paths,
    iconify_str,
    deiconify_str,
    singlenotifydispatch)
from ipywidgets import widgets as w
from traitlets import traitlets as t


class MediatorWithSingleNotifyDispatch(Mediator, t.HasTraits):
    reference = t.Unicode(default_value=None, allow_none=True)

    @singlenotifydispatch
    def notify(self, reference: Union[str, Component], change: Value) -> None:
        pass

    @notify.register("component_one")
    def _(self, reference: str, change: Value) -> None:
        self.reference = reference

    @notify.register("component_two")
    def _(self, reference: str, change: Value) -> None:
        self.reference = reference


def test_notify_dispatch():
    mediator = MediatorWithSingleNotifyDispatch()

    component_one = Component(
        mediator=mediator,
        widget=w.Button(),
        widget_name="component_one",
        names=("value",),
        notify_self=False)

    component_two = Component(
        mediator=mediator,
        widget=w.Button(),
        widget_name="component_two",
        names=("value",),
        notify_self=False)

    component_one.widget.value = True
    assert mediator.reference == "component_one"

    component_two.widget.value = True
    assert mediator.reference == "component_two"


def test_pathlib_functions():
    """"""
    root_path = pathlib.Path("/").absolute()
    iconified_root = iconify_str(IconUnicode.DIR, root_path)
    # test iconfied path str format
    assert iconified_root == f"{IconUnicode.DIR}{str(root_path.parent)[1:]}"
    # test deiconfied path str can be used as a legitimate dir Path
    assert pathlib.Path(deiconify_str(iconified_root)).is_dir()

    file_path = pathlib.Path("./tests/__init__.py").absolute()
    iconified_file = iconify_str(IconUnicode.FILE, file_path)
    assert iconified_file == f"{IconUnicode.FILE}{file_path.name}"

    def iconified_to_path(str_: str) -> pathlib.Path:
        return pathlib.Path(deiconify_str(str_)).absolute()

    # project folder Path
    project_path = pathlib.Path("./ipymediator/ipymediator").absolute()

    # recursively iterate through all project subfolders, looking for
    # all __init__.py files (rglob=True)
    iconified_dirs = directory_paths(
        project_path, pattern="__init__.py", rglob=True)

    # deiconify iconified_dirs and convert to pathlib.Path
    dir_paths = tuple(map(iconified_to_path, iconified_dirs))

    # find __init__.py within project_path (rglob=True)
    iconified_files = directory_contents(
        project_path, pattern="__init__.py", rglob=True)

    # deiconify iconified_files and convert to pathlib.Path
    file_paths = tuple(map(iconified_to_path, iconified_files))

    # iterate through each Path in dir_paths (which contain an __init__.py)
    for dir in dir_paths:
        # iterate through each Path in file_paths
        for filename in file_paths:
            # assert joining each directory and filename path refers to
            # all valid __init__.py files in the project path
            print(dir / filename)
            assert (dir / filename).is_file()

    # project tests path
    project_tests_path = pathlib.Path("./tests").absolute()

    iconified_dirs = directory_paths(
        project_tests_path, pattern="*.py", rglob=False)

    dir_paths = tuple(map(iconified_to_path, iconified_dirs))

    iconified_files = directory_contents(
        project_tests_path, pattern="*.py", rglob=False)

    file_paths = tuple(map(iconified_to_path, iconified_files))

    for dir in dir_paths:
        if dir == project_tests_path.parent:
            continue
        for filename in file_paths:
            assert (dir / filename).is_file()
