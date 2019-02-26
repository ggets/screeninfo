import enum
from dataclasses import dataclass


@dataclass
class Monitor:
    """Stores the resolution and position of a monitor."""

    x: int
    y: int
    width: int
    height: int

    def __repr__(self) -> str:
        return "monitor({}x{}+{}+{})".format(
            self.width, self.height, self.x, self.y
        )


class ScreenInfoError(Exception):
    pass


class Enumerator(enum.Enum):
    Windows = "windows"
    Cygwin = "cygwin"
    X11 = "x11"
    DRM = "drm"
    OSX = "osx"
