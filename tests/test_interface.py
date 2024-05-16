# pyright: reportGeneralTypeIssues=false, reportAttributeAccessIssue=false
from abc import ABC
from functools import singledispatchmethod
from ipymediator.interface import (
    ABCTraits, Component, Mediator, MediatorWithTraits)
from ipymediator.enumerations import Value
from ipywidgets import widgets as w
from traitlets import traitlets as t
import pytest


##############################################
# poetry run pytest --cov=ipymediator tests/ #
##############################################


class ABCTraitsWithHasTraits(ABCTraits, t.HasTraits):
    """Test traitlets.HasTraits and abc.ABC metaclass inheritance"""
    bool_trait = t.Bool(default_value=True)


class MediatorWithNotify(Mediator):
    """Test Mediator with abstract method notify"""
    def notify(self, reference: str, change: Value) -> None:
        pass


class MediatorWithoutNotify(Mediator):
    """Test concrete Mediator without notify method"""
    pass


class MediatorWithSingleDispatch(MediatorWithTraits):
    """Mediator with @singledispatchmethod to overload the
    notify reference parameter based on type."""
    reference = t.Unicode(default_value=None, allow_none=True)
    change_new = t.Bool(default_value=None, allow_none=True)

    @singledispatchmethod
    def notify(self, reference: None, change: Value) -> None:
        self.reference = None
        self.change_new = None

    @notify.register
    def _(self, reference: str, change: Value) -> None:
        """If Component initialised with notify_self=False,
        reference is widget_name property value"""
        self.reference = reference
        self.change_new = change["new"]

    @notify.register
    def _(self, reference: Component, change: Value) -> None:
        """If Component initialised with notify_self=True,
        reference is Component instance"""
        # set reference to "Component"
        self.reference = type(reference).__name__
        self.change_new = change["new"]


def test_interface_metaclass():
    """Test metaclass conflict resolution with ABCTraits"""

    with pytest.raises(TypeError) as e:
        # should raise metaclass conflict due to ABC metaclass
        # and HasTraits metaclass being of a different type
        class ABCWithHasTraits(ABC, t.HasTraits):
            pass
    assert "metaclass conflict" in str(e)

    # ABCTraits should facilitate ABC & HasTraits inheritance
    abc_traits = ABCTraitsWithHasTraits()
    assert abc_traits.has_trait("bool_trait") is True


def test_concrete_mediator():
    """Test concrete Mediator with and without notify
    abstract method implimentation"""

    with pytest.raises(TypeError):
        MediatorWithoutNotify()

    assert isinstance(MediatorWithNotify(), Mediator)


def test_concrete_component():
    """"""

    # concrete Mediator instance for concrete Components
    mediator = MediatorWithSingleDispatch()

    # test wrong trait name passed to names parameter
    with pytest.raises(ValueError) as e:
        Component(
            mediator=mediator,
            widget=w.Button(),
            widget_name="test_component",
            names=("wrong_trait",))

    err = e.value
    assert hasattr(err, '__cause__')
    assert isinstance(err.__cause__, AttributeError)

    # component_one passes widget_name as Mediator.notify reference
    component_one = Component(
        mediator=mediator,
        widget=w.Button(),
        widget_name="component_one",
        names=("value",),
        notify_self=False)

    assert component_one._mediator is mediator
    assert component_one.widget_name == "component_one"
    assert component_one._reference == component_one.widget_name
    assert "value" in component_one
    assert isinstance(component_one.widget.value, bool)

    # set component Button widget value to True
    component_one.widget.click()
    # test component __call__ to return trait value
    assert component_one("value") is True
    # test message passed to Mediator notify method from component
    assert mediator.reference == component_one.widget_name
    assert mediator.change_new is True
    assert str(component_one) == component_one.widget_name
    # test manual Component.observe_handler method
    component_one.observe_handler({"new": False})  # type: ignore
    assert mediator.change_new is False

    # component_two passes self as Mediator.notify reference
    component_two = Component(
        mediator=mediator,
        widget=w.Button(),
        widget_name=None,
        names=("value",),
        notify_self=True)

    # test widget_name default property if None on __init__
    assert component_two.widget_name == (  # ButtonComponent
        f"{type(component_two.widget).__name__}Component")
    # test _reference property is self if notify_self is True
    assert component_two._reference is component_two
    # set component_two Button widget value to True
    component_two.widget.click()
    # test message passed to Mediator notify method from component
    assert mediator.reference == "Component"
    assert mediator.change_new is True
