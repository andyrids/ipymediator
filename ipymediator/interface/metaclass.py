# import inspect
from abc import ABCMeta

from traitlets import MetaHasTraits


class ABCTraitsMeta(ABCMeta, MetaHasTraits):
    """A Metaclass combining the Abstract Base Class (ABC) Metaclass ABCMeta
    from the abc module and the traitlets library Metaclass - MetaHasTraits,
    which is the Metaclass for all DOMWidgets. This metaclass combination
    prevents ABCMeta & MetaHasTraits metaclass conflicts.

    This metaclass facilitates implimentation of interfaces through abstract
    methods (ABCMeta), whilst allowing child classes to also have traits
    (MetaHasTraits) or inherit directly from DOMWidget classes."""

    def __new__(cls, *args, **kwargs):
        return super(ABCTraitsMeta, cls).__new__(cls, *args, **kwargs)

    # def __call__(cls, *args, **kwargs):
    #     """Calls super().__init__(*args, **kwargs) for all ABCTraitsMeta
    #     users"""
    #     instance = cls.__new__(cls, *args, **kwargs)
    #     for cls_ in cls.__mro__:
    #         if isinstance(cls_, (ABCTraitsMeta)):
    #             sig = inspect.signature(cls_.__init__)
    #             kw = {n: kwargs[n] for n in sig.parameters if n in kwargs}
    #             cls_.__init__(instance, **kw)
    #     return instance


class ABCTraits(metaclass=ABCTraitsMeta):
    """Used to set ABCTraitsMeta metaclass through inheritence like abc.ABC"""

    __slots__ = ()
