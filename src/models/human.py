"""
Player base class, this class inherits object base class.

For more detailed info about the class open a terminal al type 'python -i Player.py or <file-path>'
- This will open python interpreter in interactive mode, then, to know more details type >>> help(Player)

NOTE: This class can be subclassed,
and may u want to do this to make other player object neither with special methods nor overriding any Player method.
"""

from src.models.player import Player
from src.termui import logger
from typing import List, Union, Tuple, Dict 
from time import perf_counter_ns
from pybeaut import Col


__all__: List[str] = ["Human"]  


class Human(Player):
    """Main player class with cache implementation."""

    def __init__(
        self,
        token: str,
        name: str = "Human",
        color: Col = Col.white,
    ):
        # Llamar al constructor de la clase base Player
        super().__init__(name, token, color)

    @staticmethod
    def is_bot() -> bool:
        # Definir si el jugador es un bot o no
        return False

    def addmov(self, pos: Tuple[int, int], time: Union[float, int]) -> None: 
        # Agrega rápidamente un movimiento y su tiempo a la caché
        self.cache["movements"].append(pos)
        self.cache["timings"].append(time)

    def turn(self, lang: str) -> List[Union[float, Tuple[str, str]]]: 
        """
        Método para generar un turno del jugador.
        
        - Este método no verifica si los valores son correctos, solo el tiempo del movimiento y las coordenadas retornadas como str
        para que el método constructor lo verifique.

        NOTA: ``Puede que desees sobrescribir este método en tu subclase para adaptarlo a las necesidades de la misma pero SIEMPRE DEBE DEVOLVER EL MISMO VALOR.``
        """
        
        # -- Obtenermos el logger del lenguaje seleccionado.
        _logger = logger.Logger(lang)
        
        t_start_ns = perf_counter_ns()
        posx = input(_logger.plquestion(3, self.name, self.color).format("X"))  # Coloca la coordenada {} (X o Y) idx: 3
        posy = input(_logger.plquestion(3, self.name, self.color).format("Y"))
        t_elapsed_ns = perf_counter_ns() - t_start_ns

        # -- Añadimos el movimiento y el tiempo a la caché.
        self.addmov((posx, posy), t_elapsed_ns)
        
        return [t_elapsed_ns, (posx, posy)]  #* [time, (posx, posy)]

    def _clear_cache(self) -> None:
        self.cache = self._init_cache()

    def _init_cache(self) -> Dict[str, Union[str, List[Tuple[int, int]], None]]:  
        """
        Inicializa la caché del jugador con un diccionario estático.
        - NOTA: Puede que desees sobrescribir este método para obtener una implementación de caché diferente.
        """
        return {
            "name": self._name,
            "token": self.token.strip(),
            "color": self.color,
            "movements": [],    #? Aquí solo se guarda la posición del movimiento.
            "timings": [],
            "best_timing": None,
            "worst_timing": None
        }

    def __format__(self, __format_spec: str) -> str:
        """
        Método sobrescrito especial para formatear una instancia de un jugador cuando imprimimos la instancia.
        Este método es como ``__str__`` pero decorado con un formato (__str__+.uppercase())
        
        #### Ejemplo:

        >>> p = Player("Alvaro", "X")
        >>> # queremos imprimir el nombre en verde
        >>> print(f"{p:green}")
        >>> # queremos imprimir el token en verde
        >>> print(f"{p:tkngreen})
        >>> ese método solo puede devolver el token y nombre en diferentes colores.
        """
        __format_spec = __format_spec.lower()

        if __format_spec.startswith("tkn") and __format_spec[3:] in Col:
            return f"{Col[__format_spec[3:]]}{'X' if self.btoken == 1 else '0'}{Col.reset}"

        if __format_spec not in Col:
            raise TypeError(f"Ese formato no es válido. Formatos válidos: {Col.keys()}")

        return Col[__format_spec] + self._name + Col.reset


if __name__ == "__main__":
    player1 = Human("⭕", "Alvaritow", "red")
    player2 = Human("❌", "Fanico", "blue")
    print((player1.btoken, player1.token), (player2.btoken, player2.token))
    print(f"{player2:tkngreen} ---- {player1:red} ---- {player1:white} ---- {player2:blue}")
