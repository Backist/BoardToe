
import pybeaut as pb
import sys

from src.termui import _termui
from src.models.bot import Bot
from src.i18n import AvailableLangs 
from src.core import BoardGame, BoardSize
from src.termui.logger import Logger
from src.models.human import Human
from contextlib import suppress

with suppress(KeyboardInterrupt):
    _termui.load_menu()
    
lang = input(pb.Center.XCenter(f"{pb.Col.cyan}{Logger._get_phrase('game', 0)}:  {pb.Col.reset}")).upper() #¿En que idioma desea jugar?
while lang.upper() not in AvailableLangs:
    preds = [l.upper() for l in AvailableLangs if l[0] == lang[0] or l[:-3] == lang[:-3]]
    r = input(f"You'd want to say {preds} (y/n)")
    if r.lower() in ["y", "yes"]:
        lang = preds[0]
        break #

if input(
    f"{Logger._get_phrase('game', 1, lang).format(lang)}(y/n):  {pb.Col.reset}"
).lower() not in ["yes", "y"]:
    print(f"{pb.Col.yellow}Set language to -> {pb.Col.green}ENGLISH{pb.Col.reset}")
    lang = "ENGLISH"

player1 = Human("❌", "Alvaritow", "red")
player2 = Human("❌", "Fanico", "green")

test = BoardGame(BoardSize._4X4, player1, Bot("⭕", color="red"), game_lang=lang.upper()) 

test.init_game()

    
        






    