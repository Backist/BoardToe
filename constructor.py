from utils import *
from langs import Langs
from AI.Bot import Bot
import AI.core as core


from random import choice, randint
from time import time, sleep
from datetime import datetime
from collections import namedtuple
from os import get_terminal_size
from threading import Thread

from colorama import Fore



class BoardGame:

    AVAILABLE_COLORS    = [c for c in vars(Fore).keys() if c != "RESET" or not c.endswith("_EX")]
    XCOLOR              = Fore.LIGHTRED_EX      #* static color for 'X' if player does not give any color
    OCOLOR              = Fore.LIGHTWHITE_EX    #* static color for '0' if player does not give any color
    _ptycachetuple      = namedtuple("PartyCache", ["dictmap"])


    def __init__(
        self, 
        _rows: int, 
        _columns: int, 
        tokenplayer1: str, 
        tokenplayer2: str, 
        player1: str = "player1", 
        player2: str | Bot = "player2", 
        pl1color: str = None,
        pl2color: str = None,
        game_lang: str = "SPANISH",
        game_mode: int = 1
    ):
        
        if not multiple_instcheck((_rows, _columns), int):
            raise TypeError("Rows and columns must be a numerical parameters")
        
        elif _rows != _columns or not 9 <= _rows * _columns <= 64:   #3x3 - 8x8 -> Min & max board range
            raise ValueError("The number of rows and columns must be equals or the table size is minor than 3x3 or mayor than 8x8 (Max table size of 8x8)")
        
        elif not multiple_instcheck((player1, player2), str):
            raise ValueError("Player attribute must be a string saying the name of the player")
        elif not multiple_instcheck((tokenplayer1, tokenplayer2), str) or tokenplayer1 == tokenplayer2:
            raise TypeError("Token player must be X or O and each player must define a different token")
        
        elif not (
            multiple_instcheck((player1, player2), str) or
            pl1color is not None and not pl1color.upper() in self.AVARIABLE_COLORS or 
            pl2color is not None and not pl2color.upper() in self.AVARIABLE_COLORS or 
            (pl1color.upper() == "RESET" or pl2color.upper() == "RESET")
        ):    
            raise ValueError(f"The player color must be in those list of colors: {[c.capitalize() for c in self.AVARIABLE_COLORS]}")

        
        self.rows           = _rows
        self.columns        = _columns
        self.game_lang      = game_lang
    

        self.player1        = self._make_player_cache(player1, tokenplayer1, pl1color if pl1color is not None else self.OCOLOR if tokenplayer1 == "0" else self.XCOLOR)
        self.player2        = self._make_player_cache(player2, tokenplayer2, pl2color if pl2color is not None else self.OCOLOR if tokenplayer2 == "0" else self.XCOLOR)

        self.board          = self._make_board()
        self._playing       = False
        
        self._movtuple      = namedtuple("Movement", ["token", "player_name", "position", "moviment_time"])
        #self._ptycachetuple = namedtuple("PartyCache", ["dictmap"])
        self._party_cache   = self._make_party_cache()
        self._game_cache = []
        self.debuginfo      = self._ptycachetuple(self._party_cache)

    @property
    def playing(self):
        return self._playing

    @property 
    def show_available_colors(self) -> list[str]:
        return self.AVAILABLE_COLORS


    def _make_party_cache(self) -> dict[str,]:
        "Makes a party cache."

        party_cache = {
            "board_size": (self.rows, self.columns), 
            "players": (self.player1, self.player2), 
            "party": {
                "total_time": 0,
                "win": False,    #? Cuando un jugador gana, este atributo se convierte en diccionario 
                "movements": []
            }
        }
        return party_cache
        
    """
    @classmethod
    def weak_ref() ->:
        ...
    #Me dijiste tu que lo hiciese
    """
    
    def _make_player_cache(self, player, token, color) -> dict[str,]:
        "Makes a player cache."

        cache = {
            "name": player,
            "token": token.strip().upper(),
            "color": color,
            "movements": [],    #? Aqui solo se guarda la posicion del movimiento.
            "timings": [],
            "best_timing": None,
            "worst_timing": None
        }
        return cache

    def _clear_caches(self) -> None:
        "Limpia la cache."

        player1n, tknpl1, colorpl1 = self.player1["name"], self.player1["token"], self.player1["color"]
        player2n, tknpl2, colorpl2 = self.player2["name"], self.player2["token"], self.player2["color"]

        self.player1        = self._make_player_cache(player1n, tknpl1, colorpl1)
        self.player2        = self._make_player_cache(player2n, tknpl2, colorpl2)
        self._party_cache   = self._make_party_cache()
        return


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

        t = [['-' for _ in range(self.rows)] for _ in range(self.columns)]
        return t


    def _save_win_to_cache(self, method: str):
        self._party_cache["party"]["win"] = {"method": method,}
        self._party_cache["party"]["win"]["player_name"] = self._party_cache ["party"]["movements"][-1][1]  
        #? 1 es el indice del nombre del jugador dentro de la namedtuple de Movimient


    def _pprint(self, table) -> None:
        "Prints the table in a pretty way (without colons and token-colored)"

        columns, lines = get_terminal_size().columns, get_terminal_size().lines
        print("\n")     # white line to stylize
        for i, column in enumerate(table):
            print(multiple_replace("{} {}{}".format(" "*(columns//2-self.rows//2), i+1, column), 
                    (
                        ("'", ""), 
                        (",", "  "), 
                        ("[", f"{Fore.LIGHTBLUE_EX}|{Fore.RESET} "),
                        ("]", f" {Fore.LIGHTBLUE_EX}|{Fore.RESET}"),
                        ("0", f"{self.OCOLOR}0{Fore.RESET}"), 
                        ("X", f"{self.XCOLOR}X{Fore.RESET}")
                    )
                )
            )
        print("\n")     # white line to stylize



    #! PUBLIC METHODS   ----------------------------------------------------------------

    def turn(self) -> tuple[int, int]:
        "Fuction to manage the turns"
        
        player_color = self.actual_turn["color"]

        self.turn_time = datetime.now()
        posx = input(f"{player_color}[{self.actual_turn['name']}]{Fore.RESET}: {Fore.LIGHTWHITE_EX}{Langs.get_phrase(self.game_lang, 'game', 3).format('X')} -> {Fore.RESET}") 
        #Coloca la coordenada {}
        posy = input(f"{player_color}[{self.actual_turn['name']}]{Fore.RESET}: {Fore.LIGHTWHITE_EX}{Langs.get_phrase(self.game_lang, 'game', 3).format('Y')} -> {Fore.RESET}") 
        #Coloca la coordenada {}
        self.turn_time = round((datetime.now()-self.turn_time).total_seconds(), 2)
        try:
            posx = int(posx)
            posy = int(posy)
        except:
            print(f"\n{Fore.RED}[WARNING] -> {Langs.get_phrase(self.game_lang, 'errors', 0)}{Fore.RESET}") #Las coordenadas deben ser numeros!
            return self.turn()

        if (not 1 <= posx <= self.rows) or (not 1 <= posy <= self.columns) or (not 1 <= posx <= self.rows and not 1 <= posy <= self.columns):
            print(f"\n{Fore.RED}[WARNING] -> {Langs.get_phrase(self.game_lang, 'errors', 1).format(self.rows)}{Fore.RESET}") #Las coordenadas deben estar entre 1 y {}
            return self.turn()
        
        return posx, posy
        

    def draw_board(self, table, pos: tuple[int, int], player) -> None:
        """# Importante:
            @param ``pos`` es una tupla que describe las coordenadas ``X`` e ``Y``, el orden es sumamente importante.\n
            Las coordenadas deben estar entre ``[1, board_columns] ∈ x``  --- ``[1, board_rows] ∈ y``
        """
        posx, posy = pos[0]-1, pos[1]-1


        if table[posx][posy] != "-":
            #? la posicion ya esta cogida hmmm que rico, evitamos que tenga que comprobar de que tipo es.
            print(f"\n{Fore.RED}[WARNING] -> {Langs.get_phrase(self.game_lang, 'errors', 2).format(pos, table[posx][posy])}{Fore.RESET}") #¡Ops! Esa posicion ya esta ocupada. (Posicion: {}, token: {})

            posx, posy = self.turn()
            return self.draw_board(table, (posx, posy), player)
            
                  
        elif table[posx][posy] == player["token"]:
            #? la posicion esta ocupada por una ficha del mismo tipo
            print(f"\n{Fore.RED}[WARNING] -> {Langs.get_phrase(self.game_lang, 'errors', 3)}{Fore.RESET}") #¡Ya has puesto una ficha en esta posicion!
            posx, posy = self.turn()
            return self.draw_board(table, (posx, posy), player)

        else:
            table[posx][posy] = player["token"]
            
            #? Guarda el movimiento del jugador en su cache. SOLO LAS COORDENADAS
            player["movements"].append((posx, posy))
            player["timings"].append(self.turn_time)

            self._party_cache["party"]["movements"].append(self._movtuple(player["token"], player["name"], pos, self.turn_time))
            
            _last_turn_index = self._party_cache["players"].index(self.actual_turn) #? len de la lista de jugadores (siempre 1)
            self.actual_turn = self._party_cache["players"][_last_turn_index-1]   
            #* para obtener el otro jugador se busca el indice del jugador y se le resta 1.
            return    


    def checkWin(self) -> bool:
        """
        Metodo que alberga 4 metodos independientes:
        - Horizontal
        - Vertical 
        - Diagonal en tablas par
        - Diagonal en tablas impar
        
        
        #### Metodo horizontal
        ``Si todos los elementos de una sublista de la matriz son iguales, ha ganado.``

        #### Metodo vertical:

        ``Hace un range de la longitud de la matriz con la variable i.    
        Si el elemento i de la ultima subarray no es igual al de la primera o el elemento i de
        la primera subarray es "-" se salta a la siguiente iteracion (i+1).``\n
        ``Si los elementos de los extremos son iguales, se hace un range de la matriz de nuevo menos los extremos y se guardan los valores de la sublista[_][i] en
        otra lista checks.
        Si todos los elementos de la lista checks son iguales, ha ganado un jugador.
        Si no son iguales se continua iterando.``
        """

        for subarrays in self.board:
            if subarrays[0] == "-":
                continue
            if all(elem == subarrays[0] for elem in subarrays):
                self._save_win_to_cache("Horizontal")
                return True
        

        for i in range(len(self.board)):
            if (self.board[0][i] == "-" or self.board[-1][i] == "-") or (self.board[-1][i] != self.board[0][i]):
                continue
            checks = [self.board[_][i] for _ in range(1, len(self.board)-1)]
            if all(elem == self.board[0][i] for elem in checks):
                self._save_win_to_cache("Vertical")
                return True


        #! Metodo diagonal con impares
        if len(self.board) % 2 != 0: 
            token = self.board[(len(self.board)//2)][(len(self.board)//2)]  #? centro de la matriz
        
            if token == "-":    #* si el centro de la matriz no es X o 0, no hay ninguna diagonal
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

        #! Metodo diagonal con impares
        else:
            if self.board[0][0] == "-" or self.board[0][-1] == "-":     #* Si alguna de las esquinas de las diagonales posibles esta vacia, no hay diagonales.
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

    def _checkwin2(self) -> bool:
        """Second option to make the win method"""

        bintable = core.transform2matrix(self.board)
        core.hcheck(bintable)
        core.hcheck(core.rotate_matrix(bintable))


    def checkDraw(self) -> bool:

        empty_locs = 0

        for i in range(len(self.board)):
            if any(elem == "-" for elem in self.board[i]):
                break
            if i == len(self.board)-1:
                self._save_win_to_cache("Draw")
                return True

        for i,s in zip(range(len(self.board)), range(0, len(self.board), -1)):
            if self.board[i][s] == "-":
                empty_locs += 1
        print(empty_locs)

        
        return False
                
        
    def init_game(self):
        "Game loop flow, unless you cancel the game or one player win, the game will be cancelled"

        self._clear_caches()     #* vacia la cache para iniciar una nueva partida, aunque ya se haya limpiado antes.
        self.partycounter        = datetime.now()       
        self._playing            = True
        self.actual_turn         = None

        
        def choice_start() -> None:
            self.actual_turn = choice(self._party_cache["players"])


        choice_start()

        try:
            while self._playing:
                self._pprint(self.board)
                posx, posy = self.turn()
                self.draw_board(self.board, (posx, posy), self.actual_turn)
                
                if self.checkWin():
                    self.partycounter = round((datetime.now()-self.partycounter).total_seconds())
                    self._pprint(self.board)
                    print(f"{Langs.get_phrase(self.game_lang, 'game', 2).format(self._party_cache['party']['win']['player_name'].upper())}") #¡{} ha ganado!
                    break

                if self.checkDraw():
                    self.partycounter = round((datetime.now()-self.partycounter).total_seconds())
                    self._pprint(self.board)      
                    print(f"EMPATE!!")
                    break              

                cls()

        except KeyboardInterrupt:
            print(f"\n{Fore.LIGHTYELLOW_EX}[GAME LOOP STOPED] -> {Langs.get_phrase(self.game_lang, 'runtime', 0)}{Fore.RESET}") #Se ha finalizado el juego forzosamente.
            exit()

        self.player1["best_timing"]     = min(self.player1["timings"])
        self.player1["worst_timing"]    = max(self.player1["timings"])
        self.player2["best_timing"]     = min(self.player2["timings"])
        self.player2["worst_timing"]    = max(self.player2["timings"])

        self._party_cache["party"]["total_time"] = self.partycounter
        self._game_cache.append(self._party_cache)
        self._playing = False
    
        print(self._party_cache)

        self._clear_caches()
        



if __name__ == "__main__":
    er = [
        ['', '', '0'],
        ['', '0', ''],
        ['0', '', '']
    ]

    er2 = [
        ['', '', '', '0'],
        ['', '', '0', ''],
        ['', '0', '', ''],
        ['0', '', '', '']
    ]

    er3 = [
        ['X', '', '', '', '', '0'],
        ['', 'X', '', '', '0', ''],
        ['', '', '', '0', '', ''],
        ['', '', '', 'X', '', ''],
        ['', '0', '', '', 'X', '']
        ['0', '', '', '', '', 'X']
    ]
