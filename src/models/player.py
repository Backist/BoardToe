"""
Meteclass interface that represents a Player in Boardtoe.

Copyright Backist 2022-2024 on GPL 3.0 License. See LICENSE for further details.
"""

from src import utils
from src.consts import TOKENS

from abc import ABC, abstractmethod
from datetime import datetime
from typing import MutableMapping
from pybeaut import Col



__all__: list[str] = ["Player"]


def is_valid_token(token: str):
    return token in TOKENS.values()

class Player(ABC):
    def __init__(self, name: str, token: str, color: 'Col'):
        
        # -- type checks --
        if not isinstance(name, str):
            raise TypeError(f"@name param must be a string, not {name!r} of type {type(name).__name__}")
        elif not is_valid_token(token):
            raise TypeError("@token param must be an instance of Tokens class.")
        elif color not in Col.static_colors_mapping.keys():
            raise TypeError(f"@color param must be a valid color. Valid colors: {list(Col.static_colors_mapping.keys())}")

        self._name = name
        self._token = token
        self._color = color
    
        # -- Este atributo tiene que ser declarado durante el juego
        # -- Mediante este atributo se almacena el identificador que tiene
        # -- el jugador que puede ser un 1 o 0, para comprobar los movimientos
        # -- con un sistema binario.        
        self._btoken = None
        

    @property
    def name(self) -> str:
        return self._name

    @property
    def token(self) -> str:
        return self._token

    @property
    def color(self) -> Col:
        return self._color
    
    @property
    def btoken(self) -> int:
        "Return the token as a number identifier for mathematical checks``(property)``"
        return self._btoken

    @btoken.setter
    def btoken(self, new: int):
        if -1 < new < 2:
            self._btoken = new
        else:
            raise ValueError("El token debe ser un número entre 0 y 1.")

    @abstractmethod
    def turn(self):
        """Este método debe ser implementado por las subclases."""
        pass

    @abstractmethod
    def _init_cache(self):
        """Este metodo debe ser implementado por las subclases."""
        pass

    @abstractmethod
    def _clear_cache(self):
        """Este metodo debe ser implementado por las subclases."""
        pass

    @abstractmethod
    def addmov(self, pos: tuple[int, int], time: float | int) -> None:
        pass

    @staticmethod
    @abstractmethod
    def is_bot():
        """Este método debe ser implementado por las subclases."""
        pass



