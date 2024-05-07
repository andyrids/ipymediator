import functools
import pathlib
from typing import Callable, Optional

from ipymediator.enumerations import IconUnicode


def iconify_str(icon: IconUnicode, path: pathlib.Path) -> str:
    """Return PosixPath prefixed with an Icon Enum value

    Parameters:
        icon (Icon): Icon Enum member
        path (PosixPath): PosixPath to be iconfied

    Returns:
        (str): str value with path prefixed by unicode icon
    """
    if (path_parent := path.parent).match("/"):
        path_parent = path

    icon_map = {  # for DIR, we strip the "/" prefix
        IconUnicode.DIR: f"{icon}{str(path_parent)[1:]}",
        IconUnicode.FILE: f"{icon}{path.name}",
    }

    return icon_map[icon]


def deiconify_str(iconified_path: str) -> str:
    """Clean path str prefixed with Enum unicode Icon member

    Parameters:
        iconified_path (str): iconified path to be cleaned

    Returns:
        (str): str value with unicode icon replaced by '/'
    """

    if (icon := f"{IconUnicode.DIR}") in iconified_path:
        return iconified_path.replace(icon, "/")

    icon = f"{IconUnicode.FILE}"
    return iconified_path.replace(icon, "")


def directory_paths(
    root_path: pathlib.Path, pattern: str, rglob: bool = True
) -> tuple[str, ...]:
    """"""

    def reduce_fn(acc: list[str], path: pathlib.Path) -> list[str]:
        # e.g. '📁 content'
        iconified_directory = iconify_str(IconUnicode.DIR, path)
        if iconified_directory in acc:
            return acc

        acc.append(iconified_directory)
        return acc

    iconified_root = iconify_str(IconUnicode.DIR, root_path)
    initialiser = [iconified_root]

    if rglob:
        return tuple(
            functools.reduce(reduce_fn, root_path.rglob(pattern), initialiser)
        )

    return tuple(
        functools.reduce(reduce_fn, root_path.glob(pattern), initialiser)
    )


def directory_contents(
    root_path: pathlib.Path, pattern: str, rglob: bool = True
) -> tuple[str, ...]:
    """"""

    def reduce_fn(acc: list[str], path: pathlib.Path) -> list[str]:
        if path.is_dir():
            return acc

        # e.g. '📄 file_one.csv'
        iconified_file = iconify_str(IconUnicode.FILE, path)
        if iconified_file in acc:
            return acc

        acc.append(iconified_file)
        return acc

    initialiser = list()
    if rglob:
        return tuple(
            functools.reduce(reduce_fn, root_path.rglob(pattern), initialiser)
        )
    return tuple(
        functools.reduce(reduce_fn, root_path.glob(pattern), initialiser)
    )


def singlenotifydispatch(func):
    """A class method decorator function, which replicates the logic from
    functools.singledispatchmethod, but with a function dipatch based on the
    value of the first parameter preceding self"""

    # value -> function map
    registry = dict()

    def dispatch(value: str) -> Callable:
        """Returns a function based on registry key (value)"""
        try:
            return registry[value]
        except Exception:
            return func

    def register(value: str, func: Optional[Callable] = None) -> Callable:
        """Register a function as the dipatch target based on value key"""
        if func is None:
            return lambda f: register(value, f)
        registry[value] = func
        return func

    def wrapper(*args, **kwargs):
        """Wrapper function for method decoration"""
        return dispatch(kwargs.get("reference") or args[1])(*args, **kwargs)

    # set wrapper function object properties
    wrapper.register = register
    wrapper.dispatch = dispatch
    wrapper.registry = registry

    return wrapper
