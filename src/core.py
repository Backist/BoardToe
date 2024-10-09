"""
Core of BoardToe.

This module contain the main class of Boardtoe game.


Copyright 2022-2024 Backist under license GPL 3.0.
"""



from src import utils
from src import  logger
from src import helpers
from src import i18n
from src.consts import GRID_TOKEN
from src.models.player import Player

from collections import namedtuple
from os import get_terminal_size
from datetime import datetime
from pybeaut import Col as _Col
from random import choice


class BoardSize:
    _3X3 = (3,3)
    _4X4 = (4,4)
    _5X5 = (5,5)
    _6X6 = (6,6)
    _7X7 = (7,7)
    _8X8 = (8,8)


class BoardGame:

    _movtuple      = namedtuple("Movement", ["token", "player_name", "position", "moviment_time"])
    _ptycachetuple = namedtuple("PartyCache", ["dictmap"])

    def __init__(
        self, 
        size: BoardSize | tuple[int, int],
        _player1: Player,
        _player2: Player,
        game_lang: i18n.Languages = i18n.Languages.SPANISH,
        show_stats: bool = True

    ):
        
        # -- Checks --
        if not isinstance(size, tuple) and len(size) != 2 and 3>size[0]>8 or 3>size[1]>8:
            raise ValueError("@size must be a instance of Boardsize class.")
        if game_lang not in i18n.AvailableLangs:
            raise ValueError("@game_lang must be a instance of Language class.")


        self.player1: Player = _player1
        self.player2: Player = _player2
        self.game_lang = game_lang
        self.rows = self.columns = size[0] or size[1]

        # -- Initialize instance atributes --
        self._playing = False
        self.board = None
        self.actual_turn: Player = None

        # -- Asignar un identificador de ficha a cada jugador --
        # -- Este enfoque lo que nos permite es identificar la ficha del jugador con un 1 o un 0
        # -- sin importar el tipo de ficha que el jugador este viendo en el tablero.
        # -- Cada jugador es una instancia distinta, asique pueden llamarse igual pero seran diferentes.
        self.player1.btoken = 0
        self.player2.btoken = 1


        # -- Initialize logger --
        self._logger: logger.Logger = logger.Logger(game_lang)

        if self.player1.name == "Player":
            self.player1._name = "Player1"
        if self.player2.name == "Player":
            self.player2._name = "Player2"

        self._party_cache = self._make_party_cache()
        self._game_cache  = []

        if show_stats:
            self._party_cache["Bot stats"] = []

    @property
    def playing(self):
        return self._playing

    @playing.setter
    def playing(self, new_state: bool) -> None:
        "Define si la partida esta en juego."
        self._playing = new_state

    def _make_party_cache(self) -> dict[str,]:
        "Makes a party cache."
        return {
            "board_size": (self.rows, self.columns), 
            "players": (self.player1, self.player2), 
            "party": {
                "total_time": 0,
                "win": False,    #? Cuando un jugador gana, este atributo se convierte en diccionario 
                "movements": []
            }
        }

    def _clear_caches(self, only_party: bool = False) -> None:
        """
        Limpia la cache de la partida y de cada jugador.
        
        Si ``@only_party`` es ``True``, solo la cache de la partida se limpia.
        """
        
        if only_party:
            self._party_cache = self._make_party_cache()
            return
            
        self.player1._clear_cache()
        self.player2._clear_cache()
        self._party_cache = self._make_party_cache()

    def _save_win_to_cache(self, method: str):
        self._party_cache["party"]["win"] = {"method": method}
        self._party_cache["party"]["win"]["player_name"] = self._party_cache["party"]["movements"][-1][1] 
        #? index[1] Nombre del jugador dentro de Movimient namedtuple.

    def _make_board(self) -> list:
        """``Metodo privado para crear una tabla vacia.``

        - Metodo mejorado para creacion de matrices vacias.
    
            Antes:
            >>>    t = []
            >>>    for _ in range(0, len(table)):
            >>>        t.append([])    
            >>>    for c in t:  
            >>>        c.append("-" for _ in range(0, len(table)))
            
            Despues: 
            >>> t = [['-' for _ in range(len(table))] for _ in range(len(table))]"""

        return [[GRID_TOKEN for _ in range(self.rows)] for _ in range(self.columns)]

    #! RETOCAR LA FUNCION
    def _pprint(self) -> None:
        "Prints the table in a pretty way (without colons and token-colored)"

        self.board = helpers.replace_matrix([self.board], 
                                            initial=[self.player1.token, self.player2.token], replacing=[self.player1.btoken, self.player2.btoken],
                                            reverse=True) #? la transformamos a caracteres (esta en numeros)
        
        columns, lines = get_terminal_size().columns, get_terminal_size().lines
        print("\n")     # white line to stylize
        for i, column in enumerate(self.board, 1):
            print(
                "═"*(len(self.board)-6),
                utils.multiple_replace(
                    f'{" " * (columns // 2 - self.rows // 2)} {i}{column}',
                    (
                        ("'", ""),
                        (",", "  "),
                        ("[", f"{_Col.cyan}║{_Col.reset} "),
                        ("]", f" {_Col.cyan} ║{_Col.reset} "),
                    ),
                )
            )
        print("\n")     # white line to stylize

        self.board = helpers.replace_matrix([self.board], 
                            initial=[self.player1.token, self.player2.token], replacing=[self.player1.btoken, self.player2.btoken]) 
        #? la transformamos a numeros de nuevo

    def show_stats(self):
        from pprint import pprint
        pprint(self._party_cache)
        

    
    # ** Public methods **
    def handle_turn(self) -> tuple[int, int, bool]:
        "Fuction to manage the turns"
        
        bot_cannot_turn = False
        
        if self.actual_turn.is_bot():
            turn_time, postuple, draw_detected = self.actual_turn.turn(self.board)
            if draw_detected: 
                bot_cannot_turn = True   
        else:
            turn_time, postuple = self.actual_turn.turn(self.game_lang)

        try:
            posx, posy = int(postuple[0]), int(postuple[1])

        except Exception:
            print(self._logger.error(0)) #Las coordenadas deben ser numeros!
            return self.handle_turn()

        if not 1 <= posx <= self.rows or not 1 <= posy <= self.columns:
            print(self._logger.error(1).format(self.rows)) #Las coordenadas deben estar entre 1 y {}
            return self.handle_turn()

        self.turn_time = turn_time     #? Si el turno es valido, entonces se guarda el tiempo, no antes.
        return posx, posy, bot_cannot_turn
        

    def draw_board(self, table, pos: tuple[int, int], player: Player) -> None:
        """# Importante:
            @param ``pos`` es una tupla que describe las coordenadas ``X`` e ``Y``, el orden es sumamente importante.\n
            Las coordenadas deben estar entre ``[1, board_columns] ∈ x``  --- ``[1, board_rows] ∈ y``
        """
        posx, posy = pos[0]-1, pos[1]-1

  
        if table[posx][posy] != -1:
            #? la posicion ya esta cogida, evitamos que tenga que comprobar de que tipo es.
            print(self._logger.error(2).format(pos, table[posx][posy])) #¡Ops! Esa posicion ya esta ocupada. (Posicion: {}, token: {})
            posx, posy, _ = self.handle_turn()
            return self.draw_board(table, (posx, posy), player)
            
        elif table[posx][posy] == player.btoken:
            #? la posicion esta ocupada por una ficha del mismo tipo
            print(self._logger.error(3)) #¡Ya has puesto una ficha en esta posicion!
            posx, posy, _ = self.handle_turn()
            return self.draw_board(table, (posx, posy), player)

        table[posx][posy] = player.btoken

        #? Guarda el movimiento del jugador en su cache. SOLO LAS COORDENADAS y el TIEMPO
        player.addmov(pos, self.turn_time)   
        self._party_cache["party"]["movements"].append(self._movtuple(player.token, player.name, pos, self.turn_time))
        
        _last_turn_index = self._party_cache["players"].index(self.actual_turn)
        self.actual_turn = self._party_cache["players"][_last_turn_index-1]   
        #* para obtener el otro jugador se busca el indice del jugador y se le resta 1.
        return    

    # .. Funciones que comprueban por cada movimiento si ha habido una victoria o no    
    def check_win(self) -> bool:
        """
        Verifica si se ha ganado la partida revisando:
        - Líneas horizontales.
        - Líneas verticales.
        - Diagonales en tablas de tamaño impar.
        - Diagonales en tablas de tamaño par.
        
        Returns:
            bool: True si se ha encontrado una condición de victoria, False en caso contrario.
        """
        if self._check_horizontal_win():
            return True
        if self._check_vertical_win():
            return True
        if len(self.board) % 2 == 0 and self._check_diagonal_even_board_win():
            return True
        return bool(self._check_diagonal_odd_board_win())

    def _check_horizontal_win(self) -> bool:
        """
        Verifica si alguna fila tiene todos los elementos iguales y no contiene valores vacíos (-1).
        
        Returns:
            bool: True si se detecta una victoria en una fila, False en caso contrario.
        """
        for row in self.board:
            if -1 in row:
                continue  # Si la fila contiene un espacio vacío, no es ganadora.
            if len(set(row)) == 1:  # Si todos los elementos en la fila son iguales.
                self._save_win_to_cache("Horizontal")
                return True
        return False

    def _check_vertical_win(self) -> bool:
        """
        Verifica si alguna columna tiene todos los elementos iguales y no contiene valores vacíos (-1).
        
        Returns:
            bool: True si se detecta una victoria en una columna, False en caso contrario.
        """
        for i in range(len(self.board)):
            if (self.board[0][i] == -1 or self.board[-1][i] == -1) or (self.board[0][i] != self.board[-1][i]):
                continue  # Si las esquinas de la columna no coinciden, no es ganadora.
            
            checks = [self.board[j][i] for j in range(1, len(self.board)-1)]
            if all(elem == self.board[0][i] for elem in checks):
                self._save_win_to_cache("Vertical")
                return True
        return False

    def _check_diagonal_odd_board_win(self) -> bool:
        """
        Verifica si existe una victoria diagonal en tablas de tamaño impar.
        
        Returns:
            bool: True si se detecta una victoria diagonal, False en caso contrario.
        """
        center = len(self.board) // 2
        token = self.board[center][center]  # El valor central de la tabla impar.

        if token == -1:
            return False  # Si el centro está vacío, no puede haber una diagonal ganadora.

        # Diagonal descendente (\)
        if self.board[0][0] == self.board[-1][-1] and self.board[0][0] == token:
            for i in range(1, len(self.board)-1):
                if self.board[i][i] != token:
                    break
                elif i == len(self.board)-2:
                    self._save_win_to_cache("Downwards diagonal")
                    return True

        # Diagonal ascendente (/)
        if self.board[0][-1] == self.board[-1][0] and self.board[0][-1] == token:
            for i, s in zip(range(len(self.board)-1, 1, -1), range(1, len(self.board)-1)):
                if self.board[i-1][s] != token:
                    break
                elif s == len(self.board)-2:
                    self._save_win_to_cache("Upwards diagonal")
                    return True

        return False

    def _check_diagonal_even_board_win(self) -> bool:
        """
        Verifica si existe una victoria diagonal en tablas de tamaño par.
        
        Returns:
            bool: True si se detecta una victoria diagonal, False en caso contrario.
        """
        if self.board[0][0] == -1 or self.board[0][-1] == -1:
            return False  # Si alguna de las esquinas está vacía, no puede haber una diagonal ganadora.

        # Diagonal descendente (\)
        if self.board[0][0] == self.board[-1][-1]:
            for i in range(1, len(self.board)-1):
                if self.board[i][i] != self.board[0][0]:
                    break
                elif i == len(self.board)-2:
                    self._save_win_to_cache("Downwards diagonal")
                    return True

        # Diagonal ascendente (/)
        if self.board[0][-1] == self.board[-1][0]:
            for i, s in zip(range(len(self.board)-1, 1), range(1, len(self.board)-1)):
                if self.board[i][s] != self.board[0][-1]:
                    break
                elif s == len(self.board)-2:
                    self._save_win_to_cache("Upwards diagonal")
                    return True

        return False
    
    def check_draw(self) -> bool:
        """
        Verifica si ha habido un empate segun la posicion de los tokens de cada jugador. 
        Por ahora solo verifica que ha habido un empate cuando en la tabla no hay mas posiciones libres y nadie a ganado
        """

        for i in range(len(self.board)):
            if any(elem == -1 for elem in self.board[i]):
                break
            if i == len(self.board)-1:
                return True

        empty_locs = sum(
            self.board[i][s] == -1
            for i, s in zip(range(len(self.board)), range(0, len(self.board), -1))
        )
        return False

    
    
    def init_game(self, clear_cache_when_finish: bool = True) -> str | None:
        "Game loop flow, unless you cancel the game or one player win, the game will be cancelled"

        if clear_cache_when_finish:
            self._clear_caches()     #* vacia la cache para iniciar una nueva partida, aunque ya se haya limpiado antes.  

        self.playing = True
        self.board = helpers.replace_matrix([self._make_board()])
        self.actual_turn = choice(self._party_cache["players"])

        try:
            while self.playing:
                print(helpers.matrix_view(helpers.replace_matrix([self.board], 
                                            initial=[self.player1.token, self.player2.token], replacing=[self.player1.btoken, self.player2.btoken]))) #? la transformamos a caracteres (esta en numeros)
                self.partycounter  = datetime.now()
                self._pprint()
                
                # En handle turn, siempre devolvemos una tercera variable que indica si se ha detectado un empate
                # Si el bot no es capaz de tirar ficha en su turno, es simbolo de que ha detectado un empate.
                posx, posy, draw_detected = self.handle_turn()

                if draw_detected:
                    self._pprint()
                    print(self._logger.draw(4)) # Empate en el tablero de juego.
                    break    
                
                self.draw_board(self.board, (posx, posy), self.actual_turn)

                if self.check_win():
                    self._pprint()
                    print(f"{self._logger.victory(2).format(self._party_cache['party']['win']['player_name'].upper())}") #¡{} ha ganado!
                    break

                elif self.check_draw():
                    self._pprint()
                    print(self._logger.draw(4)) # Empate en el tablero de juego.
                    break              

                utils.cls()

        except KeyboardInterrupt:
            print(self._logger.runtime(0)) #Se ha finalizado el juego forzosamente.
            exit(0)

        self.partycounter = round((datetime.now()-self.partycounter).total_seconds())

        self.player1.cache["best_timing"]  = min(self.player1.cache["timings"])
        self.player1.cache["worst_timing"] = max(self.player1.cache["timings"])
        self.player2.cache["best_timing"]  = min(self.player2.cache["timings"])
        self.player2.cache["worst_timing"] = max(self.player2.cache["timings"])

        self._party_cache["party"]["total_time"] = self.partycounter
        self._game_cache.append(self._party_cache)
        self.show_stats()
        
        self.playing = False
        self._clear_caches()

        

if __name__ == "__main__":
    
    player1 = Player("❌", "Alvaritow", "red")
    player2 = Player("⭕", "Fanico", "green")

    test = BoardGame(BoardSize._4X4, player1, player2) 

