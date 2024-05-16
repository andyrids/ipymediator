from abc import abstractmethod
from typing import Union

from ipymediator.interface.metaclass import ABCTraits
from ipymediator.enumerations import Value, Options
from traitlets import HasTraits


class Mediator(ABCTraits):
    """Abstract Mediator class for Mediator interface implimentation"""

    @abstractmethod
    def notify(
            self,
            reference: Union[str, ABCTraits],
            change: Union[Value, Options]) -> None:
        """Method for notifying a mediator class of DOMWidget trait changes

        Parameters:
            reference (str): Reference name for DOMWidget notifying Mediator

            change (Mapping): Trait changes from DOMWidget observe function
        """


class MediatorWithTraits(Mediator, HasTraits):
    """Abstract Mediator class for Mediator interface implimentation. Extends
    the Mediator interface by allowing traits from the traitlets library,
    through HasTraits inheritence.
    """
    pass
