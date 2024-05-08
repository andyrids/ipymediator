from operator import itemgetter
from typing import Optional, Union

from ipymediator.enumerations import Options, Value
from ipymediator.interface.mediator import Mediator
from ipymediator.interface.metaclass import ABCTraits

from ipywidgets import widgets
from traitlets import Bool


class Component(ABCTraits):
    """Concrete Component class for communication between a concrete Mediator
    class and a DOMWidget, based on trait changes."""

    def __new__(cls, **kwargs):
        """Add a bool value trait to any Button widgets and assigns an on_click
        function to toggle the Button value."""
        if isinstance(kwargs["widget"], widgets.Button):

            def on_click(w) -> None:
                w.value = not w.value

            kwargs["widget"].add_traits(value=Bool(False))  # type: ignore
            kwargs["widget"].on_click(on_click)
        return super(Component, cls).__new__(cls)

    def __init__(
        self,
        mediator: Mediator,
        widget: widgets.DOMWidget,
        widget_name: Optional[str] = None,
        names: tuple[str, ...] = ("value",),
        notify_self: bool = False,
    ):
        """Initialse Component class.

        Params:
            mediator (Mediator): Reference to a concrete Mediator

            widget (widgets.DOMWidget): Any widget from ipywidgets

            widget_name (str): Optional name for the Component's widget.
                If None, the default value of the widget property's class
                name + "Component" is used

            names (tuple[str, ...]): Trait names of the widget passed to
                the widget property

            notify_self (bool): Determines the reference value passed to
                Mediator's notify function - self (True) or widget_name (False)

        Raises:
            ValueError: If names param contains trait names not held by widget
        """
        self.__mediator = mediator
        self.widget = widget
        if not all(self(*names)):
            raise ValueError(
                f"traits {names} not in widget ({type(widget).__name__})")
        self.widget.observe(self.observe_handler, names=names)  # type: ignore
        self.widget_name = widget_name or f"{type(widget).__name__}Component"
        self.__reference = self if notify_self else self.widget_name

    @property
    def _mediator(self) -> Mediator:
        """Property with a reference to this Component's Mediator"""
        return self.__mediator

    @property
    def _reference(self) -> Union[str, "Component"]:
        """Store reference paramater value passed to Mediator notify method"""
        return self.__reference

    def observe_handler(self, change: Union[Value, Options]) -> None:
        """Observe callback function, passing trait changes to the Mediator"""
        self._mediator.notify(self._reference, change)

    def __call__(self, trait: str, *args):
        """Return widget trait values by leveraging __getitem__, which directs
        the call to the Component's DOMWidget properties"""
        return itemgetter(trait, *args)(self)

    def __contains__(self, item):
        """"""
        return item in self.widget

    def __getitem__(self, trait: str):
        """Subscriptable interface of Component passed to DOMWidget"""
        return getattr(self.widget, trait)

    def __setitem__(self, trait: str, value) -> None:
        """Facilitate trait value assignment with bracket notation"""
        self.widget.set_trait(trait, value)

    def __str__(self) -> str:
        """Return widget_name property value on str(object)"""
        return self.widget_name
