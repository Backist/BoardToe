"""Main bot module"""

import sys as _sys

_sys.path.append("src")

from datetime import datetime
from os import system
from random import choice, randint
from typing import MutableMapping, List, Tuple

from consts import TOKENS
from helpers import win_check
from Player import Player, _Col


def gen_random_name(size=randint(4,7)):
    vowels = 'aeiou'
    consonants = 'bcdfghjklmnpqrstvwxyz'
    
    name = []
    
    # Alternar entre consonantes y vocales para hacer el nombre legible
    for i in range(size):
        if i % 2 == 0:
            name.append(choice(consonants))
        else:
            name.append(choice(vowels))
    
    # Capitalizar la primera letra para que parezca un nombre propio
    return ''.join(name).capitalize()


class Bot(Player):
    """
    Clase que representa un Bot en el juego.
    En cada turno, se debe llamar a la función turn() para obtener el movimiento que el bot quiere realizar.
    """
    
    __fmts: dict = _Col.static_colors_mapping

    def __init__(
        self, 
        token: str,
        name: str = None,
        color: str | _Col = _Col.white,
        difficulty: str = "Easy",
        custom_doc: str = None
    ):
        """
        Inicializa un nuevo bot con los parámetros dados.
        """
        if name and not isinstance(name, str):
            raise TypeError(f"El parámetro @name debe ser una cadena, no {name!r} del tipo {type(name).__name__}")
        elif not isinstance(token, str):
            raise TypeError(f"El parámetro @token debe ser una cadena, no {token!r} del tipo {type(token).__name__}")
        elif token not in TOKENS:
            raise TypeError("Token inválido. Los tokens válidos son: '⭕' o '❌'")
        elif color not in self.__fmts:
            raise TypeError(f"Color inválido. Los colores válidos son: {self.__fmts.keys()}")
        elif difficulty.capitalize() not in {"Easy", "Normal", "Hard", "Imposible"}:
            raise TypeError(
                "La dificultad debe ser 'Easy', 'Normal', 'Hard' o 'Imposible'."
            )

        # Inicialización de atributos del bot
        self._token: str = token
        self._name: str = f"CPU: {gen_random_name()}"
        self._color: str = self.__fmts[color]
        self._difficulty: str = difficulty
        self.cache: dict | MutableMapping = self._init_cache()
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
            "token": self._token.strip(),
            "color": self._color,
            "movements": [],    # Almacena las posiciones de los movimientos realizados
            "timings": [],      # Almacena el tiempo tomado en cada turno
            "best_timing": None, # Mejor tiempo de respuesta
            "worst_timing": None, # Peor tiempo de respuesta
            "predicted_moves": [] # Movimientos predichos (solo para el bot)
        }   

    def turn(self, matrix: List[List[int]]) -> List[float | Tuple[int]]:
        """
        Calcula el movimiento del bot basado en el estado actual del tablero (matrix).
        Devuelve el tiempo transcurrido y las coordenadas del movimiento.
        """
        t_start = datetime.now()

        # Filtrar los movimientos del jugador y del bot
        moves = self.__filter_moves(
            win_check(matrix, 0 if self._token == TOKENS[0] else 1), 
            win_check(matrix, self._token), 
            len(matrix)
        )
        
        t_elapsed = (datetime.now() - t_start).microseconds

        # Si hay movimientos disponibles, elegir el mejor
        if moves:
            moves = self.__max(moves)
        else:
            input("EMPATE")  # Empate en el juego

        # Seleccionar un movimiento al azar entre las opciones posibles
        x = moves[randint(0, len(moves) - 1)]

        return [t_elapsed, (x[0] + 1, x[1] + 1)]


    # 20-08-2024: Baqueto.
    # Intento de remodelacion de la funcion con incorporacion de codigo
    # menos anidación y mejor mantenimiento de memoria usando menos listas vacias.
    # La funcion original es mas eficiente pero menos legible y escalable.
    # Originalmente hecha por @TheWisker
    def __filter_moves(
        self, 
        pmoves: List[Tuple[int, List[List[int]]]], 
        bmoves: List[Tuple[int, List[List[int]]]], 
        d: int
    ) -> List[List[int]] | None:
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
            filtered_moves[0][0] >= self.__get_difficulty(d) and randint(0, 100) % randint(1, 2) == 0
        ) else filtered_moves[0]

        return best_move[1]


    '''
    def __filter_moves(self, pmoves: List[Tuple[int, List[List[int]]]], bmoves: List[Tuple[int, List[List[int]]]], d: int) -> List[List[int]] | None:
        """
        Filtra los movimientos del bot y del jugador según la dificultad.
        Retorna los movimientos posibles o None si no hay movimientos válidos.
        """
        r: list = []
        for moves in [pmoves, bmoves]:
            if moves := [v for v in moves if v]:
                rr: list = [moves[0][0], moves[0][1]]
                for v in moves[1:]:
                    if v:
                        rr[1] = (
                            list(v[1])
                            if rr[0] > v[0]
                            else list(rr[1]) + list(v[1])
                            if rr[0] == v[0]
                            else rr[1]
                        )
                        rr[0] = min(rr[0], v[0])
                r.append(rr)
        # Retorna la lista de movimientos según la prioridad y dificultad
        return None if not r else r[0][1] if len(r) == 1 else r[1][1] if r[1][0] < r[0][0] or r[0][0] >= self.__get_difficulty(d) and randint(0, 100) % randint(1, 2) else r[0][1]
    '''
    
    def __get_difficulty(self, d: int) -> int:
        """
        Define el comportamiento del bot en función de la dificultad elegida.
        """
        if self._difficulty == "Easy":
            return 1
        elif self._difficulty == "Normal":
            return d - (d // 2)
        elif self._difficulty == "Hard":
            return d - 1
        return d
        
    def __max(self, values: List[List[int]]) -> List[List[int]] | List[int]:
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



'''
botnames = ["EUSTAQUIO", "FANICOWBELL"]


class Bot(Player):
    """
    Class instantiated on game start as a player,
    each turn the turn() function should be called to get the move that this bot wants to make.
    """
    __fmts: dict = _Col.static_cols_mapping

    def __init__(
        self, 
        token: str,
        name: str = "CPU {}",
        color: str | _Col = _Col.white,
        difficulty: str = "Easy",
        custom_doc: str = None
    ):
        if not isinstance(name, str):
            raise TypeError(f"@name param must be a string, not {name!r} of type {type(name).__name__}")
        elif not isinstance(token, str):
            raise TypeError(f"@token param must be a string, not {token!r} of type {type(token).__name__}")
        elif token not in TOKENS:
            raise TypeError("@token param is a invalid token. Valid tokens: '⭕' or '❌'")
        elif color not in self.__fmts:
            raise TypeError(f"@color param must be a valid color. Valid colors: {self.__fmts.keys()}")
        elif difficulty.capitalize() not in {"Easy", "Normal", "Hard", "Imposible"}:
            raise TypeError(
                "@difficulty param must be a valid difficulty. Valid difficulties: 'Easy', 'Normal', 'Hard', 'Imposible'"
            )

        self._token: str = token
        self._name: str = name.format(choice(botnames))     #* default 'CPU'
        self._color: str = self.__fmts[color]
        self._difficulty: str = difficulty
        self.cache: dict | MutableMapping = self._init_cache()
        self.__custom_doc__ = custom_doc if custom_doc and isinstance(custom_doc, str) else None

    def is_bot(self) -> bool:
        return True

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
            "worst_timing": None,
            "predicted_moves": [] #? Solo el bot
        }   

    def turn(self, matrix: list[list[int]]) -> list[float | tuple[int]]:
        t = datetime.now()
        moves: list[list[int]] | None = self.__filter_moves(
            win_check(matrix, 0 if self.btoken else 1), 
            win_check(matrix, self.btoken), 
            len(matrix)
        )
        t = (datetime.now()-t).microseconds
        if moves:
            moves = self.__max(moves)
        else:
            system("EMPATE")

        x = moves[randint(0 , len(moves)-1)]

        #BOT PRIORICES FUCKING PLAYER THAN HELPIN HIMSELF SOMETIMES, MAKE IT RANDOM EXCEPT ENEMY WIN
        return [t, (x[0]+1, x[1]+1)]

    def __filter_moves(self, pmoves: list[tuple[int, list[list[int]]]], bmoves: list[tuple[int, list[list[int]]]], d: int) -> list[list[int]] | None:
        r: list = []
        for moves in [pmoves, bmoves]:
            if moves := [v for v in moves if v]:
                rr: list = [moves[0][0], moves[0][1]]
                for v in moves[1:]:
                    if v:
                        rr[1] = (
                            list(v[1])
                            if rr[0] > v[0]
                            else list(rr[1]) + list(v[1])
                            if rr[0] == v[0]
                            else rr[1]
                        )
                        rr[0] = min(rr[0], v[0])
                r.append(rr)
        return None if not r else r[0][1] if len(r) == 1 else r[1][1] if r[1][0] < r[0][0] or r[0][0] >= self.__get_difficulty(d) and randint(0, 100) % randint(1, 2) else r[0][1]


    def __get_difficulty(self, d: int) -> int:
        if self._difficulty == "Easy":
            return 1
        elif self._difficulty == "Normal":
            return d - (d // 2)
        elif self._difficulty == "Hard":
            return d - 1
        return d
        
    def __max(self, values: list[list[int]]) -> list[list[int]] | list[int]:
        values = [tuple(_) for _ in values]
        r: list = [0, []]
        for v in set(values):
            c: int = values.count(v)
            r[1] = [v] if c > r[0] else r[1] + [v] if c == r[0] else r[1]
            r[0] = max(c, r[0])
        return r[1]
'''

"""
    Razonamiento logico del botico:

    Movimiento debe ser procesado de la siguiente manera: cada tipo de movimiento tendra un numero y un jugador asignado, se ejecutara el movimiento con el valor mas alto:
    0: Random move
    1: Random move en casilla adyacente a alguna del bot
    2: Cortar jugada gandora rival
    3: Ejecutar jugada gandora del bot
    Este es el metodo simple, para mayor complejidad:
    0: Random move teniendo en cuenta la mayor cantidad de casillas vacias adyacentes
    1: Random move en casilla adyacente a alguna del bot teniendo en cuenta si bloquea jugadas posteriores enemigas
    2: Cortar jugada gandora rival
    3: Ejecutar jugada gandora del bot
    Y para la mayor complejidad:
    0: Random move teniendo en cuenta la mayor cantidad de casillas vacias adyacentes
    1: Random move en casilla adyacente a alguna del bot teniendo en cuenta si bloquea jugadas posteriores enemigas y si se crea una doble posiblidad de nivel tres lo que asegura una victoria absoulta
    2: Cortar jugada gandora rival
    3: Ejecutar jugada gandora del bot


    Los posibles movimientos se conseguiran a traves de una funcion que calculara parte y delegara otra al archivo core

    Posible implementacion del cache de botico, con improbable analisis de toma de decisiones (Muy complejo)
"""