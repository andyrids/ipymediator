# ipymediator: communication between ipywidgets

## Introduction

<!-- [!TIP] [!IMPORTANT] [!WARNING] [!CAUTION] -->

> [!NOTE]
> This package is a a work in progress.

This package was created in an attempt to utlise the Mediator behavioral design pattern, to facilitate communication between ipywidgets HTML widgets, using a Mediator and Component interface. Concrete Component objects utilise these widgets through composition and automatically pass messages to a Mediator's notify method, by leaveraging its widget's `observe` method. A Component's widget, traits to observe and Mediator are passed as paramters on initialisation.

The package was inspired by [ipyfilechooser](https://github.com/crahan/ipyfilechooser/tree/master) and [leafmap](https://github.com/opengeos/leafmap) and was designed as part of a solution a specific project involving a custom ipyleaflet WidgetControl implimentation for geospatial data import.

[**ipywidgets**](https://ipywidgets.readthedocs.io/en/stable/) provides interactive HTML widgets for Jupyter notebooks and the IPython kernel.

[**traitlets**](https://traitlets.readthedocs.io/en/stable/using_traitlets.html) allows the user to define classes that have attributes (traits) with type checking and dynamically computed default values. Traitlets also implements the observer pattern and is used by ipywidgets extensively.

> [!TIP]
> Mediator dialogs built using this interface will be added to the dialogs module.

## Install

Currently this package can be installed with the following command:

`pip install git+https://github.com/AndyRids/ipymediator.git@main`

This package was built using [**Poetry**](https://python-poetry.org/docs/), which is a tool for dependency management and packaging in Python. The reposititory can be cloned and have the necessary dependancies installed using the following commands:

```bash
git clone https://github.com/AndyRids/ipymediator.git
cd ipymediator
poetry install
```


## Interface

|#| Class         | Information                                                               |
|-| ------------- | ------------------------------------------------------------------------- |
|1| ABCTraitsMeta | Metaclass combining ABCMeta[^1] and MetaHasTraits[^2] metaclasses         |
|2| ABCTraits     | Helper class that has ABCTraitsMeta as its metaclass                      |
|3| Mediator      | Abstract class defining the Mediator interface                            | 
|4| Component     | Concrete class which communicates with a Mediator                         |

[^1]: [ABCMeta](https://docs.python.org/3/library/abc.html#abc.ABCMeta)
[^2]: [traitlets](https://traitlets.readthedocs.io/en/stable/api.html#traitlets.HasTraits)

### 1. *class* ipymediator.ABCTraitsMeta

Combines standard library abc.ABCMeta metaclass and traitlets.MetaHasTraits metaclass in order to facilitate the creation of an [abstract base class](https://docs.python.org/3/glossary.html#term-abstract-base-class) (ABC), which can define a Mediator interface, and also have trait attributes provided by the traitlets library.

[^3]: [Abstract base classes](https://docs.python.org/3/glossary.html#term-abstract-base-class)

### 2. *class* ipymediator.ABCTraits

A helper class that has ABCTraitsMeta as its metaclass. With this class, an abstract base class can be created by simply deriving from ABCTraits avoiding sometimes confusing metaclass usage.

```python
from abc import abstractmethod
from ipymediator.interface import ABCTraits

class CustomABC(ABCTraits):
    pass
```

The type of ABCTraits is still `ABCTraitsMeta` - therefore inheriting from `ABCTraits` requires  precautions regarding metaclass usage, as multiple inheritance may lead to metaclass conflicts. The metaclass allows the inheritence of `traitlets.HasTraits` alongside `ABCTraits` without conflicts.

```python
from abc import abstractmethod
from ipymediator.interface import ABCTraits
from traitlets import HasTraits

class ABCWithTraits(ABCTraits, HasTraits):
    pass
```

This class would also allow the definition of an interface using an ABC that would allow inheritence of widgets from `ipywidgets` library, which utilise the `traitlets.HasTraits` class.

### 3. *class* ipymediator.Mediator

An abstract class, which impliments the Mediator interface. It requires the overriding of a `notify` abstract method, which is used by concrete Components to send messages to a Mediator.

#### Methods:

```python
@abc.abstractmethod
def notify(reference: Union[str, Component], change: dict) -> None
```
*reference* - Reference for a Component's widget notifying the Mediator. Will be a Component instance reference or a Component's `widget_name` property value.

*change* - Observed trait change `dict` from a Component's widget `observe` function. 


Abstract method for notifying a concrete Mediator of observed trait value changes, which belong to a concrete Component. The change `dict` passed to `notify` is in the following format[^4]:

[^4]: [traitlets callbacks](https://traitlets.readthedocs.io/en/stable/api.html#traitlets.observe)

```python
{
  "owner": object, # The HasTraits instance
  "new": 6, # The new value
  "old": 5, # The old value
  "name": "foo", # The name of the changed trait
  "type": 'change', # Event type of the notification
}
```

#### Example Concrete Mediator:

```python
from ipymediator.enumerations import Value
from ipymediator.interface import Mediator, Component
from ipymediator.utils import singlenotifydispatch
from ipywidgets import widgets as w
from traitlets import HasTraits, traitlets

class Dialog(Mediator, HasTraits):
    """Receives messages from Button and Text widgets and passes an action
    to carry out, to the appropriate widget on message receipt"""

    button_counter = traitlets.Integer(default_value=0, help="button clicks").tag(config=True)

    def __init__(self):
        super(Dialog, self).__init__()

        # Component adds Bool trait called value to all Button widgets by default,
        # which toggles True/False on each click (like ToggleButton widget)
        self.button_submit = Component(
            mediator=self, widget=w.Button(), widget_name="button_submit", names=("value",))

        # Component __init__ sets "value" trait to be observed by default
        self.message_clicks = Component(
            mediator=self, widget=w.Text(), widget_name="message_clicks")
        
        self.message_value = Component(
            mediator=self, widget=w.Text(), widget_name="message_value", names=("disabled",))

        # Component allows changes to widget property traits through 
        # bracket notation (see Component info for details)
        self.button_submit["description"] = "Click Me"
        self.button_submit["layout"].width = "300px"
        self.button_submit["style"].font_weight = "bold"
        self.button_submit["style"].button_color = "#f8edeb"

        self.message_clicks["style"].width = "300px"
        self.message_value["style"].width = "300px"

        self.container = w.VBox(
            children=(
                self.button_submit.widget,
                self.message_clicks.widget,
                self.message_value.widget
            )
        )

    @singlenotifydispatch
    def notify(self, reference: str, change: Value) -> None:
        """Receives messages from concrete Components.
        singlenotifydispatch wrapper allows overloading of notify
        based on reference string value.
        
        Params:
            reference (str): Reference value passed by Component. Can be used to 
                differentiate message origin.
            
            change (Value): trait value change dict passed by traitlets observe function.
        """
        pass
           
    @notify.register("button_submit")
    def _(self, reference: str, change: Value) -> None:
        """If reference == button_submit"""
        # button_submit.widget was clicked
        self.button_counter += 1
        self.message_clicks["value"] = f"Button clicks: {self.button_counter}"
        self.message_value["value"] = f"Button value is {self.button_submit['value']}"
        self.message_value["disabled"] = self.button_submit["value"]

    @notify.register("message_value")
    def _(self, reference: str, change: Value) -> None:
        """If reference == message_value"""
        # message_value.widget disabled trait change
        message = ("enabled", "disabled")[int(change["new"])]
        print(f"message_value.widget was {message}")
```
![Mediator Example](https://raw.githubusercontent.com/AndyRids/ipymediator/main/examples/images/mediator_example.png)

### 3. *class* ipymediator.Component

A concrete Component class, which communicates with a concrete Mediator implimentning the Mediator interface. Messages are passed to the Mediator by utilising a widget's observe method, which is set to use the Component's `observe_handler` method as a callback function. This callback is triggered on changes to specified widget trait(s).

Component inherits `ipymediator.ABCTraits` and can therefore be extended to inherit from `traitlets.HasTraits` and be given traits of its own without metaclass conflicts.

#### Methods:

```python
def __init__(
    mediator: Mediator, 
    widget: DOMWidget, 
    widget_name: str = None, 
    names: tuple[str, ...] = ("value",)) -> None
```
*mediator* - Reference to a Concrete Mediator.

*widget* - A widget from ipywidgets library.

*widget_name* - Optional name for the Component's widget. A default value of the widget  `__name__` + "Component" is used.

*names* - Trait names of the widget passed as the widget parameter.

*notify_self* - Determines the reference value passed to the Mediator's notify function - self (True) or widget_name (False).

The initialisation logic causes the Mediator's `notify` method to be called on changes to any of the widget traits passed as the `names` parameter. `names` must contain traits  held by the object passed to the `widget` parameter or a `ValueError` is raised.

```python
def observe_handler(change: Union[Value, Options]) -> None
```
Used as the widgets `observe` method callback function to pass a observed trait(s) change `dict` to a Mediator through its `notify` method.

#### Overriden Dunder Methods

```python
def __new__(cls, **kwargs) -> Component
```
Overriden to add a bool 'value' trait (traitlets) to any `ipywidgets.Button` passed as the `widget` initialisation parameter and assigns an `on_click` function to toggle the Button 'value' trait between True and False - Replicating 'value' trait behaviour of `ipywidgets.ToggleButton`.

> [!NOTE]
> Will likely move this logic to `ABCTraitsMeta` metaclass.

```python
def __call__(trait: str, *args)
```
Overriden to facilitate retrieval of widget trait values by leveraging `__getitem__`, which directs the call to the Component's `widget` property trait values.

> [!INFO]
> Used in `__init__` to validate widget trait names passed to `names` parameter.

```python
def __contains__(trait: str, *args)
```
Overriden to redirect trait membership tests with `in` and `not in` to the Component's `widget` property - e.g. `"value" in my_component`

```python
def __getitem__(self, trait: str)
```
Overriden to enable retreival of widget trait values on Component instance `__call__` or using using bracket notation.

```python
def __setitem__(self, trait: str, value) -> None
```
Overriden to enable setting of widget trait values through bracket notation.

```python
def __str__(self) -> str
```
Returns the value of the `widget_name` property.

## Utility Functions

### 1. *class* ipymediator.utils.singlenotifydispatch

