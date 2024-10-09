"""
Player base class, this class inherits object base class.

For more detailed info about the class open a terminal al type 'python -i Player.py or <file-path>'
- This will open python interpreter in interactive mode, then, to know more details type >>> help(Player)

NOTE: This class can be subclassed,
and may u want to do this to make other player object neither with special methods nor overriding any Player method.
"""

from src.models.player import Player 
from src import logger
from src.consts import TOKENS

from abc import ABC, abstractmethod
from datetime import datetime
from typing import MutableMapping
from pybeaut import Col


class Human(Player):
    """Main player class with cache implementation."""

    def __init__(
        self,
        token: str,
        name: str = "Human",
        color: Col = Col.white,

    ):
        super().__init__(name, token, color)

    @staticmethod
    def is_bot() -> bool:
        return False
    
    @property
    def cache_keys(self) -> list:
        "Return a list with the cache keys``(property)``"
        return list(self.cache.keys())
    @property
    def cache_size(self) -> int | float:
        "Return the size of the cache in bytes.``(property)``"
        return self.cache.__sizeof__()    

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
        _logger = logger.Logger(lang)
        t = datetime.now()
        posx = input(_logger.plquestion(3, self.name, self.color).format("X")) 
        #Coloca la coordenada {} (X o Y) idx: 3
        posy = input(_logger.plquestion(3, self.name, self.color).format("Y")) 
        t = round((datetime.now()-t).total_seconds(), 2)

        return [t, (posx, posy)]    #* [time, (posx, posy)]

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
            "token": self.token.strip(),
            "color": self.color,
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

        if __format_spec.startswith("tkn") and __format_spec[3:] in Col:
            return f"{Col[__format_spec[3:]]}{'X' if self.btoken == 1 else '0'}{Col.reset}"

        if __format_spec not in Col:
            raise TypeError(f"That format is not valid. Valid formats: {Col.keys()}")

        return Col[__format_spec]+self._name+Col.reset


if __name__ == "__main__":
    player1 = Human("⭕", "Alvaritow", "red")
    player2 = Human("❌", "Fanico", "blue")
    print((player1.btoken, player1.token),(player2.btoken, player2.token))
    print(f"{player2:tkngreen} ---- {player1:red} ---- {player1:white} ---- {player2:blue}")