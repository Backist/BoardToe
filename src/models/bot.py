"""
Bot for BoardToe.

Originally written by TheWisker.
Refactoring: Backist 20-08-2024 (Mainteinance updates.)
- - -

Razonamiento logico del botico:

Movimiento debe ser procesado de la siguiente manera: 
Cada tipo de movimiento tendra un numero y un jugador asignado, 
se ejecutara el movimiento con el valor mas alto:

0: Random move
1: Random move en casilla adyacente a alguna del bot
2: Cortar jugada gandora rival
3: Ejecutar jugada gandora del bot

Este es el metodo simple, para mayor complejidad:
0: Random move teniendo en cuenta la mayor cantidad de casillas vacias adyacentes
1: Random move en casilla adyacente a alguna del bot teniendo en cuenta si bloquea jugadas posteriores enemigas
2: Cortar jugada ganadora rival
3: Ejecutar jugada gandora del bot

Y para la mayor complejidad:
0: Random move teniendo en cuenta la mayor cantidad de casillas vacias adyacentes
1: Random move en casilla adyacente a alguna del bot teniendo en cuenta si bloquea jugadas posteriores enemigas 
    Y asi se crea una doble posiblidad de nivel tres lo que asegura una victoria absoulta.
2: Cortar jugada gandora rival
3: Ejecutar jugada gandora del bot


Los posibles movimientos se conseguiran a traves de una funcion que calculara parte y delegara otra al archivo core
Posible implementacion del cache de botico, con improbable analisis de toma de decisiones (Muy complejo)

- - -

Copyright TheWisker-Backist 2022-2024 on GPL 3.0 License. See LICENSE for further details.
"""


from src.models.player import Player
from src.tokens import TOKENS
from src.helpers import win_check
from pybeaut import Col
from time import perf_counter_ns
from random import choice, randint
from typing import List, Tuple, Union  


__all__: List[str] = ["Bot"]


def gen_random_name(size: int = randint(4, 7)) -> str: 
    vowels = 'aeiou'
    consonants = 'bcdfghjklmnpqrstvwxyz'
    
    name = []
    
    for i in range(size):
        if i % 2 == 0:
            name.append(choice(consonants))
        else:
            name.append(choice(vowels))
    
    return ''.join(name).capitalize()


class Bot(Player):
    """
    Clase que representa un Bot en el juego.
    En cada turno, se debe llamar a la función turn() para obtener el movimiento que el bot quiere realizar.
    """

    def __init__(
        self, 
        token: str = TOKENS["CIRCLE_RED"],  # Por defecto es el circulo rojo.
        name: str = "",
        color: Col = Col.white,
        difficulty: str = "Normal",
        custom_doc: str = None
    ):
        """
        Inicializa un nuevo bot con los parámetros dados.
        """
        super().__init__(name, token, color)
        
        if difficulty.capitalize() not in {"Easy", "Normal", "Hard", "Imposible"}:
            raise TypeError(
                "La dificultad debe ser 'Easy', 'Normal', 'Hard' o 'Imposible'."
            )

        self._difficulty: str = difficulty
        self.__custom_doc__ = custom_doc if custom_doc and isinstance(custom_doc, str) else None


    def is_bot(self) -> bool:
        """Retorna True indicando que este jugador es un bot."""
        return True


    def _init_cache(self) -> dict:
        """
        Inicializa el caché del jugador, guardando información relevante del estado del bot.
        """
        return {
            "name": self._name,
            "token": self._token,
            "color": self._color,
            "movements": [],   
            "timings": [],      # Tiempo de respuesta de cada turno
            "best_timing": None, 
            "worst_timing": None,
            "predicted_moves": {}  # Movimientos que el bot cree que hará el jugador en su próximo movimiento.
        }   


    def _clear_cache(self) -> None:
        "Recarga la caché del jugador, creando una nueva caché."
        self.cache = self._init_cache()
    
    
    def addmov(self, 
        pos: Tuple[int, int], time: Union[float, int],  
        turn: int,
        pred_enemy_move: Union[List[int], None] = None, 
    ) -> None:
        "Añade rápidamente un movimiento y su tiempo a la caché"
        self.cache["movements"].append(pos)
        self.cache["timings"].append(time)
        
        if pred_enemy_move is None:
            self.cache["predicted_moves"][turn] = []
        else:
            self.cache["predicted_moves"][turn] = pred_enemy_move
    
    
    def turn(self, matrix: List[List[int]], turn_counter: int) -> Tuple[float, Tuple[int], bool]: 
        """
        Calcula el movimiento del bot basado en el estado actual del tablero (matrix).
        Devuelve el tiempo transcurrido y las coordenadas del movimiento.
        
        El tiempo es calculado en nanosegundos.
        """
        
        # Cuando se juega contra el bot, el empate solo se puede computar cuando el bot
        # considere que no tiene movimientos disponibles, indicando o bien que no quedan casillas vacías
        # o bien que no hay movimientos ganadores. 
        # Cuando se juegue Human Vs Bot se deberá tomar en cuenta el tercer valor del resultado de esta función
        # para un empate.
        draw_detected = False

        t_start_ns = perf_counter_ns()
        # Filtrar los movimientos del jugador y del bot
        moves = self.__filter_moves(
            pmoves=win_check(matrix, 0 if self.btoken == 1 else 0),  # Token del jugador enemigo.
            bmoves=win_check(matrix, self.btoken), 
            board_size=len(matrix),
        )
        t_elapsed_ns = perf_counter_ns() - t_start_ns
        
        # Si hay movimientos disponibles, elegir el mejor
        if moves:
            moves = self.__max(moves)
        else:
            # Si no hay movimientos disponibles se detecta un empate.
            draw_detected = True
            return t_elapsed_ns, -1, -1, True

        # Seleccionar un movimiento al azar entre las opciones posibles
        x = moves[randint(0, len(moves) - 1)]
        
        # El tiempo de cálculo del bot es ínfimo, pero se guarda igualmente.
        self.addmov(x, t_elapsed_ns, turn_counter)
        
        return t_elapsed_ns, (x[0] + 1, x[1] + 1), draw_detected


    # ******************************************************************
    # | Functions refactoring.
    # ******************************************************************
    # 20-08-2024: Baqueto.
    # Intento de remodelación de la función con incorporación de código
    # menos anidado y mejor mantenimiento de memoria usando menos listas vacías.
    # La función original es más eficiente pero menos legible y escalable.
    # Originalmente hecha por @TheWisker
    def __filter_moves(
        self, 
        pmoves: List[Tuple[int, List[List[int]]]], 
        bmoves: List[Tuple[int, List[List[int]]]], 
        board_size: int
    ) -> Union[List[int], None]:  # Cambiado para compatibilidad con Python 3.7
        """
        Filtra los movimientos del bot y del jugador según la dificultad.
        Retorna los movimientos posibles o None si no hay movimientos válidos.
        """
        def merge_moves(moves: List[Tuple[int, List[List[int]]]]) -> List[int]:
            """ Combina y selecciona los movimientos con la menor prioridad. """
            if not moves:
                return []

            # Inicializa con el primer movimiento
            min_priority = moves[0][0]
            combined_moves = list(moves[0][1])

            # Combina movimientos con igual o menor prioridad
            for priority, move_list in moves[1:]:
                if priority < min_priority:
                    min_priority = priority
                    combined_moves = list(move_list)
                elif priority == min_priority:
                    combined_moves += list(move_list)

            return [min_priority, combined_moves]

        # Filtra movimientos no vacíos y los combina
        filtered_moves = []
        for move_set in [pmoves, bmoves]:
            valid_moves = [move for move in move_set if move]
            if valid_moves:
                filtered_moves.append(merge_moves(valid_moves))

        # Si no hay movimientos válidos, retornar None
        if not filtered_moves:
            return None

        # Retorna el mejor movimiento dependiendo de la prioridad y dificultad
        if len(filtered_moves) == 1:
            return filtered_moves[0][1]
        
        best_move = filtered_moves[1] if (
            filtered_moves[1][0] < filtered_moves[0][0] or
            filtered_moves[0][0] >= self.__get_difficulty(board_size) and randint(0, 100) % randint(1, 2) == 0
        ) else filtered_moves[0]

        return best_move[1]
    
    
    def __get_difficulty(self, board_size: int) -> int:
        """
        Define el comportamiento del bot en función de la dificultad elegida.
        """
        if self._difficulty == "Easy":
            return 1
        elif self._difficulty == "Normal":
            return board_size - (board_size // 2)
        elif self._difficulty == "Hard":
            return board_size - 1
        return board_size
    
        
    def __max(self, values: List[List[int]]) -> Union[List[List[int]], List[int]]:  # Cambiado para compatibilidad con Python 3.7
        """
        Retorna el conjunto de movimientos más frecuentes para mejorar la probabilidad de acierto.
        """
        values = [tuple(_) for _ in values]  # Convertir listas a tuplas para evitar duplicados
        r: list = [0, []]
        for v in set(values):
            c: int = values.count(v)
            r[1] = [v] if c > r[0] else r[1] + [v] if c == r[0] else r[1]
            r[0] = max(c, r[0])
        return r[1]

