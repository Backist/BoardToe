
# import pybeaut as pb
# import sys

# from src.termui import _termui
# from src.models.bot import Bot
# from src.i18n import AvailableLangs 
# from src.core import BoardGame, BoardSize
# from src.termui.logger import Logger
# from src.models.human import Human
# from contextlib import suppress

# with suppress(KeyboardInterrupt):
#     _termui.load_menu()
    
# lang = input(pb.Center.XCenter(f"{pb.Col.cyan}{Logger._get_phrase('game', 0)}:  {pb.Col.reset}")).upper() #¿En que idioma desea jugar?
# while lang.upper() not in AvailableLangs:
#     preds = [l.upper() for l in AvailableLangs if l[0] == lang[0] or l[:-3] == lang[:-3]]
#     r = input(f"You'd want to say {preds} (y/n)")
#     if r.lower() in ["y", "yes"]:
#         lang = preds[0]
#         break #

# if input(
#     f"{Logger._get_phrase('game', 1, lang).format(lang)}(y/n):  {pb.Col.reset}"
# ).lower() not in ["yes", "y"]:
#     print(f"{pb.Col.yellow}Set language to -> {pb.Col.green}ENGLISH{pb.Col.reset}")
#     lang = "ENGLISH"

# player1 = Human("❌", "Alvaritow", "red")
# player2 = Human("❌", "Fanico", "green")

# test = BoardGame(BoardSize._4X4, player1, Bot("⭕", color="red"), game_lang=lang.upper()) 

# test.init_game()



import curses
import time
import threading
import random

from src.termui.banners import BANNER
from src.termui._termui import loading_anim
from src.termui._termui import load_menu


def create_box(frase):
    longitud = len(frase) + 4
    return (
        '╭' + '─' * (longitud) + '╮' + '\n'
        f'│  {frase}  │' + '\n'
        '╰' + '─' * (longitud) + '╯' + '\n'
    )


# Datos del juego compartidos
class GameData:
    def __init__(self):
        self.timer = 0
        self.player1 = 'X'
        self.player2 = 'O'
        self.last_move = 'None'
        self.win_probability = random.randint(0, 100)
        self.board = [['-' for _ in range(3)] for _ in range(3)]  # Tablero inicializado con guiones
        self.running = True
        self.maximized = False
        self.input_str = ""


# Timer que se ejecuta en la ventana derecha
def start_timer(game_data, update_event):
    while game_data.running:
        time.sleep(1)
        game_data.timer += 1
        update_event.set()


# Actualiza la ventana derecha con el timer y datos del juego
def update_right_window(right_window, game_data):
    right_window.clear()
    right_window.box()

    max_y, max_x = right_window.getmaxyx()
    timer_text = f" Timer: {game_data.timer}s "
    right_window.attron(curses.color_pair(2))
    right_window.addstr(0, (max_x - len(timer_text)) // 2, timer_text)
    right_window.attroff(curses.color_pair(2))

    game_data_text = [
        f"Player 1: {game_data.player1}",
        f"Player 2: {game_data.player2}",
        f"Last move: {game_data.last_move}",
        f"Win probability: {game_data.win_probability}%"
    ]

    for i, line in enumerate(game_data_text):
        right_window.addstr(2 + i, 2, line, curses.color_pair(2))

    right_window.refresh()


# Actualiza la ventana izquierda con el tablero de juego
def update_left_window(left_window, game_data):
    left_window.clear()
    left_window.box()

    # Tablero centrado usando el nuevo diseño
    board = game_data.board
    max_y, max_x = left_window.getmaxyx()

    # Construir el tablero en el formato especificado
    board_lines = []
    board_lines.append("┏━━━┳━━━┳━━━┓")
    
    for i in range(3):
        row = '   ┃   '.join(board[i])  # Combina las columnas de la fila
        board_lines.append(f"┃ {row} ┃")  # Añadir márgenes laterales
        if i < 2:  # Añadir línea divisoria entre filas
            board_lines.append("┣━━━╋━━━╋━━━┫")

    board_lines.append("┗━━━┻━━━┻━━━┛")

    # Añadir el tablero a la ventana, asegurando que la alineación sea correcta
    for i, line in enumerate(board_lines):
        left_window.addstr((max_y // 2 - 3) + i, (max_x - len(line)) // 2, line, curses.color_pair(1))

    # Input para coordenadas del turno
    input_prompt = create_box("Introduce tu coordenada -> ")

    # Añadir cada línea de la caja de input
    for idx, line in enumerate(input_prompt.splitlines()):
        left_window.addstr(max_y - 4 + idx, 2, line, curses.color_pair(1))
    
    left_window.addstr(max_y - 1, 2, game_data.input_str, curses.color_pair(1))  # Agregar lo que se está introduciendo

    left_window.refresh()


# Nueva función para capturar la entrada del usuario sin bloquear
def get_player_input(stdscr, game_data, left_window, prompt, key):
    if key == curses.ERR:
        return

    if key == 10:  # Enter
        return game_data.input_str

    elif key == 27:  # ESC
        game_data.input_str = ""
        return None

    elif key == 127:  # Retroceso
        game_data.input_str = game_data.input_str[:-1]
    elif 32 <= key <= 126:  # Teclas imprimibles
        game_data.input_str += chr(key)

    update_left_window(left_window, game_data)  # Actualizar la ventana con la entrada
    return None


# Función principal para el programa
def main(stdscr):
    curses.curs_set(1)  # Mostrar el cursor
    stdscr.nodelay(True)  # Hacer que getch sea no bloqueante
    stdscr.timeout(100)   # Timeout para getch en milisegundos

    # Configuración de colores
    curses.start_color()
    curses.init_pair(1, curses.COLOR_RED, curses.COLOR_BLACK)    # Ventana izquierda
    curses.init_pair(2, curses.COLOR_GREEN, curses.COLOR_BLACK)  # Ventana derecha
    curses.init_pair(3, curses.COLOR_CYAN, curses.COLOR_BLACK)   # Mensajes

    # Configuración de las ventanas
    max_y, max_x = stdscr.getmaxyx()
    half_x = max_x // 2

    left_window = curses.newwin(max_y, half_x, 0, 0)
    right_window = curses.newwin(max_y, max_x - half_x, 0, half_x)

    # Datos del juego
    game_data = GameData()

    # Evento para actualizar ventanas
    update_event = threading.Event()

    # Hilo para el temporizador
    timer_thread = threading.Thread(target=start_timer, args=(game_data, update_event), daemon=True)
    timer_thread.start()

    # Ciclo principal
    while game_data.running:
        if update_event.is_set():
            update_right_window(right_window, game_data)
            update_event.clear()

        update_left_window(left_window, game_data)

        # Obtener entrada del usuario mientras el juego sigue actualizándose
        key = stdscr.getch()
        player_input = get_player_input(stdscr, game_data, left_window, create_box("Introduce la coordenada -> "), key)

        if player_input is not None:
            game_data.last_move = player_input
            game_data.input_str = ""  # Reiniciar la cadena para el siguiente input

        if key == ord('q'):
            game_data.running = False
        elif key == ord('s'):
            if not game_data.maximized:
                left_window.resize(max_y, max_x)
                left_window.mvwin(0, 0)
                left_window.clear()
                left_window.box()
                left_window.refresh()

                right_window.clear()
                right_window.refresh()
                game_data.maximized = True
            else:
                left_window.resize(max_y, half_x)
                left_window.mvwin(0, 0)
                left_window.clear()
                left_window.box()
                left_window.refresh()

                right_window.resize(max_y, max_x - half_x)
                right_window.mvwin(0, half_x)
                right_window.clear()
                right_window.box()
                update_right_window(right_window, game_data)
                game_data.maximized = False

        time.sleep(0.1)  # Pequeña pausa para evitar alto uso de CPU

    # Finalizar curses
    curses.curs_set(1)


# Ejecutar la aplicación curses
if __name__ == "__main__":
    curses.wrapper(main)

    
        






    