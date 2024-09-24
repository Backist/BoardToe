"""
Player base class, this class inherits object base class.

For more detailed info about the class open a terminal al type 'python -i Player.py or <file-path>'
- This will open python interpreter in interactive mode, then, to know more details type >>> help(Player)

NOTE: This class can be subclassed,
and may u want to do this to make other player object neither with special methods nor overriding any Player method.
"""

from utils import *
from consts import *
from logger import *

from datetime import datetime
from typing import MutableMapping

from pybeaut import Col as _Col


__all__ = ["Player"]


class Player(object):
    """Main player class with cache implementation."""
    
    __fmts: dict = _Col.static_cols_mapping

    def __init__(
        self,
        token: str,
        name: str = "Player",
        color: str | _Col = _Col.white,

    ):
        if not isinstance(name, str):
            raise TypeError(f"@name param must be a string, not {name!r} of type {type(name).__name__}")
        elif not isinstance(token, str):
            raise TypeError(f"@token param must be a string, not {token!r} of type {type(token).__name__}")
        elif token not in TOKENS:
            raise TypeError("@token param is a invalid token. Valid tokens: '⭕' or '❌'")
        elif color not in self.__fmts:
            raise TypeError(f"@color param must be a valid color. Valid colors: {self.__fmts.keys()}")

        self._name:    str   = name     #* default 'Player'
        self._token:   str   = token
        self._color:   str   = self.__fmts[color]
        self.cache:  dict | MutableMapping = self._init_cache()

    @property
    def name(self) -> str:
        "Return the name of the player in a read-only view ``(property)``"
        return self._name
    @property
    def color(self) -> _Col | str:
        "Return the color of the player in a read-only view ``(property)``"
        return self._color
    @property
    def token(self) -> str:
        "Return the token of the player in a read-only view ``(property)``"
        return self._token
    @property
    def btoken(self) -> int:
        "Return the token as a number (0 for 0, 1 for X) ``(property)``"
        return 1 if self._token == XTOKEN else 0
    @property
    def cache_keys(self) -> list:
        "Return a list with the cache keys``(property)``"
        return list(self.cache.keys())
    @property
    def cache_size(self) -> int | float:
        "Return the size of the cache in bytes.``(property)``"
        return self.cache.__sizeof__()

    @staticmethod
    def subclasses() -> list:
        "Lazy method to show all subclasses of this class"
        return Player.__subclasses__()
    
    def is_bot(self) -> bool:
        return False

    def _clear_cache(self) -> None:
        "Reload the player cache, makes a new cache."
        self.cache = self._init_cache()

    def _init_cache(self) -> dict[str]:
        """
        Initialize the player cache with an static dictionary.
        - NOTE: You may want to override this method to get a different cache implementation
        """
        return {
            "name": self._name,
            "token": self._token.strip(),
            "color": self._color,
            "movements": [],    #? Aqui solo se guarda la posicion del movimiento.
            "timings": [],
            "best_timing": None,
            "worst_timing": None
        }
            
    def __format__(self, __format_spec: str) -> str:
        """Special overrided method to format a instance of a player when we print the instance.
        This method is a ``__str__`` method but it's decorated with a format (__str__+.uppercase())
        
       #### Example:

        >>> p = Player("Alvaro", "X")
        >>> # we want to print the name in green
        >>> print(f"{p:green}")
        >>> # we want to print the token in green
        >>> print(f"{p:tkngreen})
        >>> that method only can return the token & name in different colors.
        """
        __format_spec = __format_spec.lower()

        if __format_spec.startswith("tkn") and __format_spec[3:] in self.__fmts:
            return f"{self.__fmts[__format_spec[3:]]}{'X' if self.btoken == 1 else '0'}{_Col.reset}"

        if __format_spec not in self.__fmts:
            raise TypeError(f"That format is not valid. Valid formats: {self.__fmts.keys()}")

        return self.__fmts[__format_spec]+self._name+_Col.reset

    def addmov(self, pos: tuple[int, int], time: float | int) -> None:
        "Add in a fast method one movement and it's time in the cache"
        self.cache["movements"].append(pos)
        self.cache["timings"].append(time)
    
    
    def turn(self, lang: str) -> list[float | tuple[str, str]]:
        """
        Method to generate a turn to the player.
        
        - This method does not check if the values are correct, only for the time of the move and the coordinates returned in str
        for the constructor method to check.

        NOTE: ``You may want to overwrite this method in your subclass to adapt it to the needs of the subclass but it MUST ALWAYS RETURN THE SAME VALUE.``
        """
        _logger = Logger(lang)
        t = datetime.now()
        posx = input(_logger.plquestion(3, self.name, self.color).format("X")) 
        #Coloca la coordenada {} (X o Y) idx: 3
        posy = input(_logger.plquestion(3, self.name, self.color).format("Y")) 
        t = round((datetime.now()-t).total_seconds(), 2)

        return [t, (posx, posy)]    #* [time, (posx, posy)]



if __name__ == "__main__":
    player1 = Player("⭕", "Alvaritow", "red")
    player2 = Player("❌", "Fanico", "blue")
    print((player1.btoken, player1.token),(player2.btoken, player2.token))
    print(f"{player2:tkngreen} ---- {player1:red} ---- {player1:white} ---- {player2:blue}")
