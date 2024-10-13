"""
Modulo que contiene las funciones vitales para mostrar el juego en la terminal.
Aunque no está terminado, está pensado para contener todas las animaciones de texto
únicamente. Luego este archivo se llama en el main.py, que lleva el flujo del programa y donde 
corre curses.

Backest-TheWisker 2022-2024 under GPL 3.0 License. See LICENSE for details.
"""


import textwrap

# from click import secho, echo, echo_via_pager, confirm, pause
from src.constants import IS_WINDOWS
from pybeaut import Box, Colorate, Cursor, Col
from contextlib import suppress
from pynput import keyboard
from time import sleep
from random import randint
from os import get_terminal_size, system
from getpass import getpass
from typing import List, Union


class SkipAnimationTrigger:
    def __init__(self, skip_key: str):
        self.skip_key = skip_key
        self.skip_animation = False

    def on_press(self, key):
        with suppress(AttributeError):   # Ignora teclas especiales
            if key.char == self.skip_key:
                self.skip_animation = True

    def start_listener(self):
        with keyboard.Listener(on_press=self.on_press) as listener:
            listener.join()


def padding(width: int): return print(" "*width)
def cls(): return system("cls") if IS_WINDOWS else system("clear")

def loading_anim(repeats: int = 3, interval: float = 0.1, delay: float = 0.25, 
                 color: Col = Col.cyan, hc: bool = True) -> None:
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
        Cursor.HideCursor()  

    for _ in range(repeats):
        for i in range(len(load_dots_str)):
            output = f"{color}{load_dots_str[:i+1]}" if color else load_dots_str[:i+1]
            print(output, end="\r")
            sleep(interval)

        print(" " * len(load_dots_str), end="\r")  
        sleep(delay)  

    sleep(0.1) 
    
    if hc:
        Cursor.ShowCursor() 



def reveal_anim(t: str, interval: Union[int,float] = 0.03, pause_comma: float = 0.2, pause_dot: float = 0.4, 
                color: Col = Col.reset, center: bool = False, adjust_content: bool = True, skip_key: str = 's') -> None:
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


    # Iniciar el listener para la tecla de salto
    animation = SkipAnimationTrigger(skip_key)
    listener = keyboard.Listener(on_press=animation.on_press)
    listener.start()

    # Revelar el texto poco a poco o saltarlo si se pulsa la tecla de salto
    for char in t:
        if animation.skip_animation: 
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
    print(Col.reset)



def make_box(fields: List[str], color: Col = Col.white, btitle: str = None, 
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
            return Colorate.Horizontal(color, Box.SimpleCube("\n".join(t)))
        return Box.SimpleCube("".join(t))
    
    return Colorate.Color(color, Box.DoubleCube(f"{btitle}\n") + Box.DoubleCube("".join(t)) if color else Box.SimpleCube(f"{btitle}\n")+ "\n" + pb.Box.DoubleCube("".join(t)))




if __name__ == "__main__":
    print(Box.SimpleCube(Colorate.Horizontal(Col.blue_to_cyan, "Title", 2, 3)))
    print(Box.DoubleCube(f"{Colorate.Horizontal(Col.blue_to_cyan, 'Title', 2, 3)}"))