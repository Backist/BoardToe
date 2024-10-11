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
from src.constants import TOKENS, TokenID
from src.helpers import win_check, rotate_matrix
from pybeaut import Col
from time import perf_counter_ns
from random import choice, randint
from typing import List, Tuple

__all__: List[str] = ["Bot"]

def gen_random_name(size=randint(4,7)):
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
    
    # Variable de comprobacion de version para debug.
    v2: bool = True

    def __init__(
        self, 
        token: str = TOKENS[TokenID.CIRCLE_RED], # Por defecto es el circulo rojo.
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


    @staticmethod
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
            "predicted_moves": {} # Movimientos que el bot cree que har'a el jugador en su proximo movimiento.
        }   


    def _clear_cache(self) -> None:
        "Reload the player cache, makes a new cache."
        self.cache = self._init_cache()
    
    
    def addmov(self, 
        pos: tuple[int, int], time: float | int,
        turn: int,
        pred_enemy_move: list | None, 
    ) -> None:
        "Add in a fast method one movement and it's time in the cache"
        self.cache["movements"].append(pos)
        self.cache["timings"].append(time)
        
        if pred_enemy_move is None:
            self.cache["predicted_moves"][turn] = []
        else:
            self.cache["predicted_moves"][turn] = pred_enemy_move
    
    
    def turn(self,matrix: List[List[int]], enemy_movs_cache, turn_counter: int) -> Tuple[float, Tuple[int], bool]:
        """
        Calcula el movimiento del bot basado en el estado actual del tablero (matrix).
        Devuelve el tiempo transcurrido y las coordenadas del movimiento.
        
        El tiempo es calculado en nano segundos.
        """
        
        # Cuando se juega contra el bot, el empate solo se puede computar cuando el bot
        # considere no tiene movimientos disponibles, indicando o bien no quedan casillas vacias
        # o bien que no hay movimientos ganadores. 
        # Cuando se juegue Human Vs Bot se debera tomar en cuenta el tercer valor del resultado de esta funcion
        # para un empate.
        draw_detected = False

        t_start_ns = perf_counter_ns()
        # Filtrar los movimientos del jugador y del bot
        moves, enemy_predict_movs = self.__filter_moves(
            pmoves=win_check(matrix, 0 if self.btoken == 1 else 0),   # Token del jugador enemigo.
            bmoves=win_check(matrix, self.btoken), 
            matrix=matrix,
            board_size=len(matrix),
            enemy_movs_cache=enemy_movs_cache
        )
        t_elapsed_ns = perf_counter_ns() - t_start_ns

        # Si hay movimientos disponibles, elegir el mejor
        if moves:
            moves = self.__max(moves)
        else:
            # Si no hay movimientos disponibles se detecta un empate.
            draw_detected = True
            return t_elapsed_ns,-1,-1,True

        # Seleccionar un movimiento al azar entre las opciones posibles
        x = moves[randint(0, len(moves) - 1)]
        
        # El tiempo de calculo del bot en infimo, pero se guarda igualmente.
        self.addmov(x, t_elapsed_ns, turn_counter, enemy_predict_movs)
        
        return t_elapsed_ns, (x[0] + 1, x[1] + 1), draw_detected



    # ******************************************************************
    # | Functions refactoring.
    # ******************************************************************
    # 20-08-2024: Baqueto.
    # Intento de remodelacion de la funcion con incorporacion de codigo
    # menos anidación y mejor mantenimiento de memoria usando menos listas vacias.
    # La funcion original es mas eficiente pero menos legible y escalable.
    # Originalmente escrita por @TheWisker

    def predict_move_from_cache(self, enemy_moves: list[list[int]], matrix: list[list[int]]):
        """
        Predice el próximo movimiento del jugador enemigo basándose en sus movimientos previos guardados en caché.
        """
        if not enemy_moves:
            # Si no hay movimientos previos, no se puede hacer una predicción
            return []

        # Busca patrones en la caché, por ejemplo, si el jugador tiende a completar filas o columnas
        for move in enemy_moves:
            row, col = move
            # Check si el jugador tiende a completar filas o columnas
            if matrix[row].count(-1) > 0:  # Hay espacio en la fila
                return [row, matrix[row].index(-1)]
            rotated_matrix = rotate_matrix(matrix)
            if rotated_matrix[col].count(-1) > 0:  # Hay espacio en la columna
                return [rotated_matrix[col].index(-1), col]

        # for i, row in enumerate(matrix):
        #     if -1 in row:
        #         return [i, row.index(-1)]

        # return []
        
        # Usamos next en este caso.
        return next(
            ([i, row.index(-1)] for i, row in enumerate(matrix) if -1 in row), []
        )


    # -- Nueva funcion ver.2024
    def player_moves_on_diagonal(self, diagonal: list[int], player_moves: list[list[int]]) -> bool:
        """
        Verifica si el jugador está ocupando activamente una diagonal.
        """
        return any(i == j for i, j in player_moves if diagonal[i] == -1)
        #! Arreglar


    # -- Nueva funcion ver.2024
    def advanced_predict_move(self, player_moves: list[list[int]], matrix: list[list[int]], bot_moves: list[list[int]]) -> list[int]:
        """
        Predice el próximo movimiento del jugador basándose en patrones más avanzados, 
        como la ocupación de filas, columnas y diagonales.
        """
        # Analizar diagonales principales y secundarias
        main_diag = [matrix[i][i] for i in range(len(matrix))]
        sec_diag = [matrix[i][len(matrix) - i - 1] for i in range(len(matrix))]

        # Revisar si hay espacios disponibles en las diagonales y si el jugador tiende a usarlas
        if main_diag.count(-1) > 0 and self.player_moves_on_diagonal(main_diag, player_moves):
            return [main_diag.index(-1), main_diag.index(-1)]  # Predicción en la diagonal principal
        elif sec_diag.count(-1) > 0 and self.player_moves_on_diagonal(sec_diag, player_moves):
            return [sec_diag.index(-1), len(matrix) - sec_diag.index(-1) - 1]  # Predicción en la diagonal secundaria

        # Si no hay un patrón diagonal claro, usar otras predicciones
        return self.predict_move_from_cache(player_moves, matrix)
    
    
    def __filter_moves(
        self, 
        pmoves: List[Tuple[int, List[List[int]]]], 
        bmoves: List[Tuple[int, List[List[int]]]], 
        matrix: list[list[int]],  
        board_size: int, 
        enemy_movs_cache: list[list[int]], 
    ) -> Tuple[List[List[int]] | None, List[List[int]] | None]:
        """
        Filtra los movimientos del bot y del jugador enemigo según la dificultad elegida.
        Añade predicción de movimientos del jugador basada en la caché de movimientos.
        """
        def merge_moves(moves: List[Tuple[int, List[List[int]]]]) -> List[int]:
            """ Combina y selecciona los movimientos con la menor prioridad. """
            if not moves:
                return []

            min_priority = moves[0][0]
            combined_moves = list(moves[0][1])

            for priority, move_list in moves[1:]:
                if priority < min_priority:
                    min_priority = priority
                    combined_moves = list(move_list)
                elif priority == min_priority:
                    combined_moves += list(move_list)

            return [min_priority, combined_moves]

        filtered_moves = []
        for move_set in [pmoves, bmoves]:
            valid_moves = [move for move in move_set if move]
            if valid_moves:
                filtered_moves.append(merge_moves(valid_moves))

        if not filtered_moves:
            return None, None  # No hay movimientos válidos

        # Predicción de movimiento del jugador enemigo basada en su caché
        predicted_player_move = self.predict_move_from_cache(enemy_movs_cache, matrix)

        # Selección de movimiento del bot
        best_move = filtered_moves[1] if (
            filtered_moves[1][0] < filtered_moves[0][0] or
            filtered_moves[0][0] >= self.__get_difficulty(board_size) and randint(0, 100) % randint(1, 2) == 0
        ) else filtered_moves[0]

        return best_move[1], predicted_player_move


    def __get_difficulty(self, board_size: int) -> int:
        """
        Define la dificultad del bot en funcion al tama;o del tablero de juego.
        Ajusta la profundidad de análisis y la probabilidad de cometer errores.
        """
        if self._difficulty == "Easy":
            # El bot comete errores más facilmente, ignora algunos posibles movimientos del jugador
            error_margin = randint(1, 3)  
            return max(1, board_size - error_margin)  # Se asegura de que no sea menor a 1
        elif self._difficulty == "Normal":
            # Ajustando la dificultad a la cuarta parte, puede cometer errores ocasionalmente
            error_margin = randint(0, board_size // 4)  
            return max(1, board_size - error_margin)  # Reduce ligeramente el análisis
        elif self._difficulty == "Hard":
            # El bot analiza la mayoría de los movimientos del jugador y predice más acertadamente
            return max(1, board_size - 1)  # Solo comete errores si hay múltiples posibilidades iguales
        return board_size

        
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
