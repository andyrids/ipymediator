from abc import abstractmethod
from typing import Union

from metaclass import ABCTraits
from custom_types import Value, Options

from traitlets import HasTraits

class Mediator(ABCTraits):
    """Abstract Mediator class for Mediator interface implimentation"""

    @abstractmethod
    def notify(self, reference: str, change: Union[Value, Options]) -> None:
        """Method for notifying a mediator class of DOMWidget trait changes

        Parameters:
            reference (str): Reference name for DOMWidget notifying Mediator

            change (Mapping): Trait changes from DOMWidget observe function
        """
        pass

class DialogMediator(Mediator, HasTraits):
    """Abstract Mediator class for Mediator interface implimentation. A
    DialogMediator extends the Mediator interface implimentation by adding
    traitlet library traits.

    Traits:
        dialog_open (bool): Dialog open/closed flag

        dialog_selection (pathlib.Path): Selected file path

    Abstract methods:
        notify: From Mediator class

        _control: Holds a reference to a DialogMediator control Mediator
    """
    dialog_open = traitlets.Bool(default_value=True).tag(sync=True) # type: ignore
    dialog_selection = traitlets.Instance(pathlib.Path, allow_none=True, default_value=None).tag(sync=True) # type: ignore