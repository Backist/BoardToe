"""
Este módulo contiene funciones para estilizar la salida de datos por la terminal, como
directorios en forma de tabla y colorida, entre otros tipos de datos.
"""
from typing import Union
from src.termui.colors import Color, TrueColor, Style, ResetSequence


def clprint(
    target: str,
    color: Union[Color,TrueColor],
    style: Style,
    reset: ResetSequence
):
    ...