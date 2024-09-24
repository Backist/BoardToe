from utils import *
from logger import *
from consts import EMPTOKEN
from Player import Player
import core

from random import choice
from datetime import datetime
from collections import namedtuple
from os import get_terminal_size

from pybeaut import Col as _Col



class BoardGame:

    _movtuple           = namedtuple("Movement", ["token", "player_name", "position", "moviment_time"])
    _ptycachetuple      = namedtuple("PartyCache", ["dictmap"])

    def __init__(
        self, 
        size: tuple[int, int],
        _player1: Player,
        _player2: Player,
        game_lang: str = "SPANISH",
        show_stats: bool = True

    ):
        
        if not isinstance(size, (tuple, list)):
            raise TypeError("@size must be a tuple or list containing w numerical values (rows and columns)")
        elif not all(isinstance(e, int) for e in size) or len(size) != 2:
            raise TypeError("The list have more than 2 values or rows and columns must be a numerical parameters")
        elif size[0] != size[1] or not 9 <= size[0] * size[1] <= 64:   #3x3 - 8x8 -> Min & max board range
            raise ValueError("The number of rows and columns must be equals or the table size is minor than 3x3 or mayor than 8x8 (Max table size of 8x8)")

        elif game_lang not in AVAILABLE_LANGS:
            raise TypeError(f"The selected language '{repr(game_lang)}' is not set yet!")

        self.rows = self.columns = size[0] or size[1]
        self.board              = None

        self.player1: Player    = _player1
        self.player2: Player    = _player2


        if self.player1.token == self.player2.token:
            raise ValueError(f"The players have the same token ({self.player1.token!r})!!")
        if self.player1.name == "Player":
            self.player1._name = "Player1"
        if self.player2.name == "Player":
            self.player2._name = "Player2"

        self.game_lang          = game_lang
        self._logger: Logger    = Logger(game_lang)
        self._playing           = False

        self._party_cache       = self._make_party_cache()
        self._game_cache        = []

        if show_stats:
            self._party_cache["Bot stats"] = []

    @property
    def playing(self):
        return self._playing

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


    def _clear_caches(self) -> None:
        "Limpia la cache."
        self.player1._clear_cache()
        self.player2._clear_cache()
        self._party_cache   = self._make_party_cache()


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

        return [[EMPTOKEN for _ in range(self.rows)] for _ in range(self.columns)]


    def _save_win_to_cache(self, method: str):
        self._party_cache["party"]["win"] = {"method": method}
        self._party_cache["party"]["win"]["player_name"] = self._party_cache["party"]["movements"][-1][1]  
        #? 1 es el indice del nombre del jugador dentro de la namedtuple de Movimient


    #! RETOCAR LA FUNCION
    def _pprint(self) -> None:
        "Prints the table in a pretty way (without colons and token-colored)"

        self.board = core.replace_matrix([self.board], reverse=True) #? la transformamos a caracteres (esta en numeros)
        columns, lines = get_terminal_size().columns, get_terminal_size().lines
        print("\n")     # white line to stylize
        for i, column in enumerate(self.board):
            print(
                multiple_replace(
                    f'{" " * (columns // 2 - self.rows // 2)} {i + 1}{column}',
                    (
                        ("'", ""),
                        (",", "  "),
                        ("[", f"{_Col.cyan}║{_Col.reset} "),
                        ("]", f" {_Col.cyan} ║{_Col.reset} "),
                    ),
                )
            )
        print("\n")     # white line to stylize

        self.board = core.replace_matrix([self.board]) #? la transformamos a numeros de nuevo

    def show_stats(self) -> str | dict[str,]:
        print(self._party_cache)
        

    #! PUBLIC METHODS   ----------------------------------------------------------------
    

    def handle_turn(self) -> tuple[int, int]:
        "Fuction to manage the turns"

        if self.actual_turn.is_bot():
            turn_time, postuple = self.actual_turn.turn(self.board)   
        else:
            turn_time, postuple = self.actual_turn.turn(self.game_lang)

        try:
            posx, posy = int(postuple[0]), int(postuple[1])

        except:
            print(self._logger.error(0)) #Las coordenadas deben ser numeros!
            return self.handle_turn()

        if not 1 <= posx <= self.rows or not 1 <= posy <= self.columns:
            print(self._logger.error(1).format(self.rows)) #Las coordenadas deben estar entre 1 y {}
            return self.handle_turn()

        self.turn_time = turn_time     #? Si el turno es valido, entonces se guarda el tiempo, no antes.
        return posx, posy
        

    def draw_board(self, table, pos: tuple[int, int], player: Player) -> None:
        """# Importante:
            @param ``pos`` es una tupla que describe las coordenadas ``X`` e ``Y``, el orden es sumamente importante.\n
            Las coordenadas deben estar entre ``[1, board_columns] ∈ x``  --- ``[1, board_rows] ∈ y``
        """
        posx, posy = pos[0]-1, pos[1]-1

  
        if table[posx][posy] != -1:
            #? la posicion ya esta cogida, evitamos que tenga que comprobar de que tipo es.
            print(self._logger.error(2).format(pos, table[posx][posy])) #¡Ops! Esa posicion ya esta ocupada. (Posicion: {}, token: {})
            posx, posy = self.handle_turn()
            return self.draw_board(table, (posx, posy), player)
            
        elif table[posx][posy] == player.btoken:
            #? la posicion esta ocupada por una ficha del mismo tipo
            print(self._logger.error(3)) #¡Ya has puesto una ficha en esta posicion!
            posx, posy = self.handle_turn()
            return self.draw_board(table, (posx, posy), player)

        table[posx][posy] = player.btoken

        #? Guarda el movimiento del jugador en su cache. SOLO LAS COORDENADAS y el TIEMPO
        player.addmov(pos, self.turn_time)   
        self._party_cache["party"]["movements"].append(self._movtuple(player.token, player.name, pos, self.turn_time))
        
        _last_turn_index = self._party_cache["players"].index(self.actual_turn)
        self.actual_turn = self._party_cache["players"][_last_turn_index-1]   
        #* para obtener el otro jugador se busca el indice del jugador y se le resta 1.
        return    

    ## .. Funciones que comprueban por cada movimiento si ha habido una victoria o no
    '''
    def checkWin(self) -> bool:
        """
            Metodo que alberga 4 metodos independientes:
            - Horizontal
            - Vertical 
            - Diagonal en tablas par
            - Diagonal en tablas impar
        """
        
        for subarrays in self.board:
            if -1 in subarrays:
                continue
            elif len(set(subarrays)) == 1:
                self._save_win_to_cache("Horizontal")
                return True
        
        for i in range(len(self.board)):
            if (self.board[0][i] == -1 or self.board[-1][i] == -1) or (self.board[-1][i] != self.board[0][i]):
                continue
            checks = [self.board[_][i] for _ in range(1, len(self.board)-1)]
            if all(elem == self.board[0][i] for elem in checks):
                self._save_win_to_cache("Vertical")
                return True

        #! Metodo diagonal con impares
        if len(self.board) % 2 != 0: 
            token = self.board[(len(self.board)//2)][(len(self.board)//2)]  #? centro de la matriz
        
            if token == -1:    #* si el centro de la matriz no es X o 0, no hay ninguna diagonal
                return False

            if self.board[0][0] == self.board[-1][-1] and self.board[0][0] == token:
                for i in range(1, len(self.board)-1):  #* evitamos pasar otra vez por las esquinas que sabemos que son iguales. 
                    if self.board[i][i] != token:
                        break
                    elif i == len(self.board)-2:   #* Si la ultima iteracion i es igual a la longitud de la tabla-2, quiere decir que todas las iteraciones anteriores son True, formando una diagonal.
                        self._save_win_to_cache("Downwards diagonal")
                        return True

            if self.board[0][-1] == self.board[-1][0] and self.board[0][-1] == token:
                for i,s in zip(range(len(self.board)-1, 1, -1), range(1, len(self.board)-1), strict=True):
                    if self.board[i-1][s] != token:
                        break
                    elif s == len(self.board)-2:   #* Si la ultima iteracion i es igual a la longitud de la tabla-2, quiere decir que todas las iteraciones anteriores son True, formando una diagonal.
                        self._save_win_to_cache("Upwards diagonal")
                        return True

        #! Metodo diagonal con pares
        else:
            if self.board[0][0] == -1 or self.board[0][-1] == -1:     #* Si alguna de las esquinas de las diagonales posibles esta vacia, no hay diagonales.
                return False

            if self.board[0][0] == self.board[-1][-1]:
                for i in range(1, len(self.board)-1):  #* evitamos pasar otra vez por las esquinas que sabemos que son True
                    if self.board[i][i] != self.board[0][0]:
                        break
                    elif i == len(self.board)-2:   #* Si la ultima iteracion i es igual a la longitud de la tabla-2 
                        #* (la posicion anterior a la esquina que no cuenta), quiere decir que todas las iteraciones anteriores son True, formando una diagonal.
                        self._save_win_to_cache("Downwards diagonal")
                        return True

            if self.board[0][-1] == self.board[-1][0]:
                for i,s in zip(range(len(self.board)-1,1), range(1, len(self.board)-1)):
                    if self.board[i][s] != self.board[0][0]:    #* si alguna del medio no es igual a la primera, no es diagonal.
                        break
                    elif s == len(self.board)-2:  
                        self._save_win_to_cache("Upwards diagonal")
                        return True
        return False
    '''        
    
    def checkWin(self) -> bool:
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
        if len(self.board) % 2 != 0:
            # Tablas de tamaño impar
            if self._check_diagonal_odd_board_win():
                return True
        else:
            # Tablas de tamaño par
            if self._check_diagonal_even_board_win():
                return True
        
        return False

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


    def checkDraw(self) -> bool:
        "Verifica si ha habido un empate. Por ahora solo verifica que ha habido un empate cuando en la tabla no hay mas posiciones libres y nadie a ganado"
        for i in range(len(self.board)):
            if any(elem == -1 for elem in self.board[i]):
                break
            if i == len(self.board)-1:
                self._save_win_to_cache("Draw")
                return True

        empty_locs = sum(
            self.board[i][s] == -1
            for i, s in zip(range(len(self.board)), range(0, len(self.board), -1))
        )
        return False
                
        
    def init_game(self) -> str | None:
        "Game loop flow, unless you cancel the game or one player win, the game will be cancelled"

        self._clear_caches()     #* vacia la cache para iniciar una nueva partida, aunque ya se haya limpiado antes.  

        self.board: list[list]          = core.replace_matrix([self._make_board()])
        self._playing: bool             = True
        self.actual_turn: Player        = choice(self._party_cache["players"])

        try:
            while self._playing:
                self.partycounter  = datetime.now()

                self._pprint()
                posx, posy = self.handle_turn()

                self.draw_board(self.board, (posx, posy), self.actual_turn)

                if self.checkWin():
                    self.partycounter = round((datetime.now()-self.partycounter).total_seconds())
                    self._pprint()
                    print(f"{self._logger.victory(2).format(self._party_cache['party']['win']['player_name'].upper())}") #¡{} ha ganado!
                    break

                elif self.checkDraw():
                    self.partycounter = round((datetime.now()-self.partycounter).total_seconds())
                    self._pprint()
                    print("EMPATE!!")
                    break              

                cls()

        except KeyboardInterrupt:
            print(self._logger.runtime(0)) #Se ha finalizado el juego forzosamente.
            exit()

        self.player1.cache["best_timing"]     = min(self.player1.cache["timings"])
        self.player1.cache["worst_timing"]    = max(self.player1.cache["timings"])
        self.player2.cache["best_timing"]     = min(self.player2.cache["timings"])
        self.player2.cache["worst_timing"]    = max(self.player2.cache["timings"])

        self._party_cache["party"]["total_time"] = self.partycounter
        self._game_cache.append(self._party_cache)
        self._playing = False
        self.show_stats()

        self._clear_caches()

        

if __name__ == "__main__":
    ...
