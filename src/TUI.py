from pybeaut import Col as _Col, Center, Cursor, Colorate, Box, Add, Write
from random import randint
from os import get_terminal_size
from time import sleep
from getpass import getpass
from consts import *
from utils import *


TERMSIZE: list[int, int] = [get_terminal_size().columns, get_terminal_size().lines]
#TODO ///////////////////////////////////////      TUI SECTION        ////////////////////////////////////////////////

#! Mirar el modulo 'climage' de python. Es un manejador de imagenes que convierte la imagen a su codigo de escape ansi.
#! Si el sistema es UNIX, se ofrece mejor compatibilidad con el modulo 'term-image'.

#! ///////////////////////////////  BUG IMPORTANTE  //////////////////////////////////
#! Cuando ejecutas el juego en una powershell o una terminal, si mientras esta haciendo la animacion del texto, seleccionas con el raton o le das al enter
#! por ejemplo 5 veces, la animacion deja de escribir texto y aparece directamente el mensaje del lenguaje o directamente se rompe.

#! /////////////////////////////////// BUG IMPORTANTE 2     //////////
#! Cuando no encuentra el lenguaje y hace una prediccion del lenguaje que queria decir pero no hay matches, coje el indice 0 pero no hay matches y
#! se para porque no encuentra lenguaje.




#& ************  DYNAMIC FUNCS **************

def loading_anim(repeats: int = 3, interval: int = 0.1, delay: int = 0.25, color: _Col = None, hc: bool = True) -> None:
    """Crea una animacion de cargar.\n## Parametros.\n
    - @repeats: Las veces que repite la animacion de carga 
    - @interval: Tiempo de espera entre cada punto
    - @delay: Tiempo de espera entre repeticiones.
    - @color: Color para la animacion de carga.
    - @hc: Esconde el cursor si es ``True``"""
    
    _ = "• • •"

    if hc:
        Cursor.HideCursor()
    def loop():
        for i in range(len(_)):
            print(f"{color}{_[:i+1]}", end= "\r") if color is not None else print(_[:i+1], end= "\r")
            sleep(interval)
    
    for r in range(repeats):
        loop()
        print(" "*len(_), end= "\r") #clean terminal once a loop finalized.
        sleep(delay)
    sleep(0.1)      #? smooth exit
    if hc:
        Cursor.ShowCursor()

def padding(width: int):
    return print(" "*width)

def reveal_anim(t: str, color: _Col = None, interval: int | float = 0.05, overlap: bool = False, center: bool = False, adjust_content: bool = False) -> None:
    """Genera una animacion de texto donde las letras se van revelando poco a poco. 
    ``Metodo recursivo.``
    """

    if center:
        if adjust_content:
            for i in adjust_content(t):
                reveal_anim(i, color, interval, overlap)
        for i in t.splitlines(True):
            reveal_anim(i, color, interval, overlap)
    elif adjust_content:
        for i in adjust_content(t):
            reveal_anim(i, color, interval, overlap)

    for i in range(len(t)):
        print(f"{color}{t[:i+1]}", end="\r") if color is not None else print(t[:i+1], end="\r")
        sleep(interval)

        if t[i] == "\n":
            if not overlap:
                print("\r")
            reveal_anim(t[i+1:], color, interval)
            break
    print(_Col.reset)
    return 


def adjust_content(text: str, termlen: int = get_terminal_size().columns) -> list[str]:
    fraction = round(len(text) / termlen)
    if fraction < 2:        #? si el resultado de la division es 0.xx se redondea a 1
        return [text]
    _ = []
    for _ in range(fraction):
        e = text[:termlen+1]
        _.append(e)
        text = text[termlen+1:]
    return _


        

#& ************  TUI WRAPPERS **************

def _make_box(fields: list[str], color: _Col = _Col.white, btitle: str = None, enum: bool = False, simplecube: bool = False):
 
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
            return Colorate.Horizontal(color, Box.SimpleCube("\n".join(t)))
        return Box.SimpleCube("".join(t))
    
    return Colorate.Color(color, Box.DoubleCube(f"{btitle}\n") + Box.DoubleCube("".join(t)) if color else Box.SimpleCube(f"{btitle}\n")+ "\n" + Box.DoubleCube("".join(t)))


print(_make_box(["asa", "asd"], btitle="Hika"))
def load_menu():
    "Load the splash frame"

    Cursor.HideCursor()
    loading_anim(randint(2, 3), color= _Col.cyan, hc=False)

    cls()    
    getpass(Colorate.Horizontal(_Col.blue_to_cyan, "Press Enter Key to continue. . ."))
    cls()

    print(Colorate.Horizontal(_Col.blue_to_cyan, BANNER))
    padding(3)
    reveal_anim(SPLASH_TEXT, adjust_content= True)
    Cursor.ShowCursor()

def config_menu():
    ...

def load_game():
    config_menu()
    
print(Box.SimpleCube(Colorate.Horizontal(_Col.blue_to_cyan, "Title", 2, 3)))
print(Box.DoubleCube(f"{_Col.blue}Loading. . .{_Col.reset}"))