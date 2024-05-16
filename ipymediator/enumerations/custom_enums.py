from enum import Enum


class ButtonColour(str, Enum):
    """StrEnum for button widget colours"""

    BLUE: "ButtonColour.BLUE.value" = "#cce6f4"
    GREEN: "ButtonColour.GREEN.value" = "#ebebeb"
    RED: "ButtonColour.RED.value" = "#f8edeb"

    def __str__(self) -> str:
        """Enables StrEnum prior to 3.11"""
        return str.__str__(self)


class IconUnicode(str, Enum):
    """StrEnum for unicode icons 📁 & 📄"""

    DIR = "\U0001F4C1"
    FILE = "\U0001F4C4"

    def __str__(self) -> str:
        """Enables StrEnum prior to 3.11"""
        return str.__str__(self)

    def __format__(self, spec) -> str:
        """Right-pad space for f-string calls"""
        return f"{self.value} "
