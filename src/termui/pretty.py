

from typing import Union
from src.termui.colors import Color, TrueColor, Style, ResetSequence


def clprint(
    target: str,
    color: Union[Color,TrueColor],
    style: Style,
    reset: ResetSequence
):
    ...