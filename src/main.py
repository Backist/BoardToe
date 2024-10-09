
import pybeaut as pb
import console

from IA import Bot 
from contextlib import suppress
from core import BoardGame
from logger import Logger
from i18n import AVAILABLE_LANGS
from player import Player




if __name__ == "__main__":

    with suppress(KeyboardInterrupt):
        console.load_menu()
        
    lang = input(pb.Center.XCenter(f"{pb.Col.cyan}{Logger._get_phrase('game', 0)}:  {pb.Col.reset}")).upper() #¿En que idioma desea jugar?
    while lang.upper() not in AVAILABLE_LANGS:
        preds = [l.upper() for l in AVAILABLE_LANGS if l[0] == lang[0] or l[:-3] == lang[:-3]]
        r = input(f"You'd want to say {preds} (y/n)")
        if r.lower() in ["y", "yes"]:
            lang = preds[0]
            break #

    if input(
        f"{Logger._get_phrase('game', 1, lang).format(lang)}(y/n):  {pb.Col.reset}"
    ).lower() not in ["yes", "y"]:
        print(f"{pb.Col.yellow}Set language to -> {pb.Col.green}ENGLISH{pb.Col.reset}")
        lang = "ENGLISH"

    player1 = Player("❌", "Alvaritow", "red")
    player2 = Player("❌", "Fanico", "green")

    test = BoardGame((4,4), player1, Bot("⭕", color="red"), game_lang=lang.upper()) 

    test.init_game()

    
        






    