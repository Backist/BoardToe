import pybeaut as pb
import textwrap
import keyboard
from time import sleep
from random import randint
from os import get_terminal_size

from getpass import getpass
from consts import *
from utils import *


def padding(width: int): return print(" "*width)


def loading_anim(repeats: int = 3, interval: float = 0.1, delay: float = 0.25, 
                 color: pb.Colors = pb.Col.cyan, hc: bool = True) -> None:
    """
    Crea una animación de carga.

    ## Parámetros.
    - @repeats: Las veces que repite la animación de carga.
    - @interval: Tiempo de espera entre cada punto.
    - @delay: Tiempo de espera entre repeticiones.
    - @color: Color para la animación de carga.
    - @hc: Esconde el pb.cursor si es ``True``.
    """

    load_dots_str = "• " * 3 

    if hc:
        pb.pb.Cursor.Hidepb.Cursor()  

    for _ in range(repeats):
        for i in range(len(load_dots_str)):
            output = f"{color}{load_dots_str[:i+1]}" if color else load_dots_str[:i+1]
            print(output, end="\r")
            sleep(interval)

        print(" " * len(load_dots_str), end="\r")  
        sleep(delay)  

    sleep(0.1) 
    
    if hc:
        pb.pb.Cursor.Showpb.Cursor() 



def reveal_anim(t: str, interval: int | float = 0.03, pause_comma: float = 0.2, pause_dot: float = 0.4, 
                color: pb.Col = pb.Colors.reset, center: bool = False, adjust_content: bool = True, skip_key: str = 's') -> None:
    """
    Genera una animación de texto donde las letras se van revelando poco a poco, con la posibilidad de
    saltar la animación pulsando una tecla específica.
    
    :param t: Texto a revelar.
    :param interval: Tiempo (en segundos) entre la aparición de cada carácter.
    :param pause_comma: Tiempo de pausa al encontrar una coma.
    :param pause_dot: Tiempo de pausa al encontrar un punto.
    :param center: Centra el texto en la terminal si es True.
    :param adjust_content: Ajusta el texto al ancho de la terminal si es True.
    :param skip_key: Tecla para saltar la animación.
    """
    
    # Ajustar el contenido al ancho de la terminal
    if adjust_content:
        term_width = get_terminal_size().columns
        t = '\n'.join(textwrap.wrap(t, width=term_width))

    if center:
        t = '\n'.join(line.center(get_terminal_size().columns // 2, "\t") for line in t.splitlines())

    # Mensaje de advertencia sobre la tecla de salto
    print(f"[Press '{skip_key.upper()}' to skip.]")

    # Revelar el texto poco a poco o saltarlo si se pulsa la tecla de salto
    for char in t:
        if keyboard.is_pressed(skip_key): 
            print("\nSkipping animation...\n")
            return 
        
        print(f"{color}{char}", end="", flush=True)

        # Pausa según el tipo de carácter
        if char == ',':
            sleep(pause_comma)
        elif char == '.':
            sleep(pause_dot)
        else:
            sleep(interval)
    
    # Asegura el final de animacion correctamente
    # e resetea el color en caso de haber usado uno.
    print(pb.Col.reset)


    

def _make_box(fields: list[str], color: pb.Col = pb.Col.white, btitle: str = None, 
              enum: bool = False, simplecube: bool = False) -> str:
 
    t = []
    # if btitle is not None:
    #     t.append(f"{btitle}\n")
    
    for i in range(len(fields)):
        if enum:
            t.append(f"[{i+1}] {fields[i]}")
        else:
            t.append(f"{fields[i]}")
    
    if simplecube:
        if color:
            return pb.Colorate.Horizontal(color, pb.Box.SimpleCube("\n".join(t)))
        return pb.Box.SimpleCube("".join(t))
    
    return pb.Colorate.Color(color, pb.Box.DoubleCube(f"{btitle}\n") + pb.Box.DoubleCube("".join(t)) if color else pb.Box.SimpleCube(f"{btitle}\n")+ "\n" + pb.Box.DoubleCube("".join(t)))


def load_menu():
    "Load the splash frame"

    pb.Cursor.HideCursor()
    loading_anim(randint(2, 3), color= pb.Col.cyan, hc=False)

    cls()    
    getpass(pb.Colorate.Horizontal(pb.Col.blue_to_cyan, "Press Enter Key to continue. . ."))
    cls()

    print(pb.Colorate.Horizontal(pb.Col.blue_to_cyan, BANNER))
    padding(3)
    reveal_anim(SPLASH_TEXT, adjust_content= True, center=True)
    pb.Cursor.ShowCursor()

def config_menu():
    ...

def load_game():
    config_menu()
    
print(pb.Box.SimpleCube(pb.Colorate.Horizontal(pb.Col.blue_to_cyan, "Title", 2, 3)))
print(pb.Box.DoubleCube(f"{pb.Colorate.Horizontal(pb.Col.blue_to_cyan, 'Title', 2, 3)}"))