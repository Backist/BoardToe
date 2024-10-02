from contextlib import suppress
from consts import *
from utils import *
from AI.Bot import *
from core import BoardGame
from logger import Logger
from langs import AVAILABLE_LANGS
from Player import Player, _Col
from console import *
import pybeaut as pb


if __name__ == "__main__":

    with suppress(KeyboardInterrupt):
        load_menu()
        
    lang = input(pb.Center.XCenter(f"{_Col.cyan}{Logger._get_phrase('game', 0)}:  {_Col.reset}")).upper() #¿En que idioma desea jugar?
    while lang.upper() not in AVAILABLE_LANGS:
        preds = [l.upper() for l in AVAILABLE_LANGS if l[0] == lang[0] or l[:-3] == lang[:-3]]
        r = input(f"You'd want to say {preds} (y/n)")
        if r.lower() in ["y", "yes"]:
            lang = preds[0]
            break #

    if input(
        f"{Logger._get_phrase('game', 1, lang).format(lang)}(y/n):  {_Col.reset}"
    ).lower() not in ["yes", "y"]:
        print(f"{_Col.yellow}Set language to -> {_Col.green}ENGLISH{_Col.reset}")
        lang = "ENGLISH"

    player1 = Player("❌", "Alvaritow", "red")
    player2 = Player("❌", "Fanico", "green")

    test = BoardGame((4,4), player1, Bot("⭕", color="red", difficulty="imposible"), game_lang=lang.upper()) 

    test.init_game()

    
        






    