"""
Game constants
"""

# This implementation introduces the `TokenName` class to provide constant names for tokens 
# in the `Token` class. This change reduces string errors by ensuring consistent references 
# to token names, improving code maintainability and readability.
class TokenID:
    CIRCLE_RED_FILL = "CIRCLE_RED_FILL"
    CIRCLE_RED = "CIRCLE_RED"
    CIRCLE_ORANGE = "CIRCLE_ORANGE"
    CIRCLE_YELLOW = "CIRCLE_YELLOW"
    CIRCLE_GREEN = "CIRCLE_GREEN"
    CIRCLE_BLUE = "CIRCLE_BLUE"
    CIRCLE_PURPLE = "CIRCLE_PURPLE"
    CIRCLE_BROWN = "CIRCLE_BROWN"
    CIRCLE_BLACK = "CIRCLE_BLACK"
    CIRCLE_WHITE = "CIRCLE_WHITE"
    SQUARE_RED = "SQUARE_RED"
    SQUARE_ORANGE = "SQUARE_ORANGE"
    SQUARE_YELLOW = "SQUARE_YELLOW"
    SQUARE_GREEN = "SQUARE_GREEN"
    SQUARE_BLUE = "SQUARE_BLUE"
    SQUARE_PURPLE = "SQUARE_PURPLE"
    SQUARE_BROWN = "SQUARE_BROWN"
    SQUARE_BLACK = "SQUARE_BLACK"
    SQUARE_WHITE = "SQUARE_WHITE"
    CROSS_BLACK = "CROSS_BLACK"
    CROSS_RED = "CROSS_RED"

TOKENS = {    
    TokenID.CIRCLE_RED: "⭕",
    TokenID.CIRCLE_RED_FILL: "🔴", 
    TokenID.CIRCLE_ORANGE: "🟠",
    TokenID.CIRCLE_YELLOW: "🟡",
    TokenID.CIRCLE_GREEN: "🟢",
    TokenID.CIRCLE_BLUE: "🔵",
    TokenID.CIRCLE_PURPLE: "🟣",
    TokenID.CIRCLE_BROWN: "🟤",
    TokenID.CIRCLE_BLACK: "⚫",
    TokenID.CIRCLE_WHITE: "⚪",
    TokenID.SQUARE_RED: "🟥",
    TokenID.SQUARE_ORANGE: "🟧",
    TokenID.SQUARE_YELLOW: "🟨",
    TokenID.SQUARE_GREEN: "🟩",
    TokenID.SQUARE_BLUE: "🟦",
    TokenID.SQUARE_PURPLE: "🟪",
    TokenID.SQUARE_BROWN: "🟫",
    TokenID.SQUARE_BLACK: "⬛",
    TokenID.SQUARE_WHITE: "⬜",
    TokenID.CROSS_BLACK: "✖️",
    TokenID.CROSS_RED: "❌"
}
    
class EmojiID:
    GEARWHEEL = "GEARWHEEL"
    MEGAPHONE = "MEGAPHONE"
    LOCK = "LOCK"
    STOP_SIGNAL = "STOP_SIGNAL"
    EXCLAMATION = "EXCLAMATION"
    LOUDSPEAKER = "LOUDSPEAKER"
    TIE = "TIE"
    ROBOTIC_ARM = "ROBOTIC_ARM"
    FIRST_MEDAL = "FIRST_MEDAL"
    CUP = "CUP"
    ROBOT = "ROBOT"
    MAGNIFYING_GLASS = "MAGNIFYING_GLASS"
    QUESTION = "QUESTION"

# Pre-generated dictionary with emoji names mapped to their corresponding emoji characters
EMOJIS = {
    EmojiID.GEARWHEEL: "⚙️",
    EmojiID.MEGAPHONE: "📢",
    EmojiID.LOCK: "🔒",
    EmojiID.STOP_SIGNAL: "⛔️",
    EmojiID.EXCLAMATION: "❕",
    EmojiID.LOUDSPEAKER: "🔊",
    EmojiID.TIE: "🤝",
    EmojiID.ROBOTIC_ARM: "🦾",
    EmojiID.FIRST_MEDAL: "🥇",
    EmojiID.CUP: "🏆",
    EmojiID.ROBOT: "🤖",
    EmojiID.MAGNIFYING_GLASS: "🔍",
    EmojiID.QUESTION: "❔",
}



# -- Token reservado para las divisiones del tablero.
GRID_TOKEN = "➖"
CROSS_TOKEN   = TOKENS[TokenID.CROSS_RED]
CIRCLE_TOKEN   = TOKENS[TokenID.CIRCLE_RED]

#TODO ///////////////////////////////////////       WELCOME TEXT BANNERS        ////////////////////////////////////////////////

BANNER = r"""
 /$$$$$$$                                      /$$ /$$$$$$$$                 
| $$__  $$                                    | $$|__  $$__/                 
| $$  \ $$  /$$$$$$   /$$$$$$   /$$$$$$   /$$$$$$$   | $$  /$$$$$$   /$$$$$$ 
| $$$$$$$  /$$__  $$ |____  $$ /$$__  $$ /$$__  $$   | $$ /$$__  $$ /$$__  $$
| $$__  $$| $$  \ $$  /$$$$$$$| $$  \__/| $$  | $$   | $$| $$  \ $$| $$$$$$$$
| $$  \ $$| $$  | $$ /$$__  $$| $$      | $$  | $$   | $$| $$  | $$| $$_____/
| $$$$$$$/|  $$$$$$/|  $$$$$$$| $$      |  $$$$$$$   | $$|  $$$$$$/|  $$$$$$$
|_______/  \______/  \_______/|__/       \_______/   |__/ \______/  \_______/
"""

BANNER2 = r"""
██████╗  ██████╗  █████╗ ██████╗ ██████╗ ████████╗ ██████╗ ███████╗
██╔══██╗██╔═══██╗██╔══██╗██╔══██╗██╔══██╗╚══██╔══╝██╔═══██╗██╔════╝
██████╔╝██║   ██║███████║██████╔╝██║  ██║   ██║   ██║   ██║█████╗  
██╔══██╗██║   ██║██╔══██║██╔══██╗██║  ██║   ██║   ██║   ██║██╔══╝  
██████╔╝╚██████╔╝██║  ██║██║  ██║██████╔╝   ██║   ╚██████╔╝███████╗
╚═════╝  ╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═╝╚═════╝    ╚═╝    ╚═════╝ ╚══════╝"""

BANNER3 = r"""
 ███████████     ███████      █████████   ███████████   ██████████   ███████████    ███████    ██████████
░░███░░░░░███  ███░░░░░███   ███░░░░░███ ░░███░░░░░███ ░░███░░░░███ ░█░░░███░░░█  ███░░░░░███ ░░███░░░░░█
 ░███    ░███ ███     ░░███ ░███    ░███  ░███    ░███  ░███   ░░███░   ░███  ░  ███     ░░███ ░███  █ ░ 
 ░██████████ ░███      ░███ ░███████████  ░██████████   ░███    ░███    ░███    ░███      ░███ ░██████   
 ░███░░░░░███░███      ░███ ░███░░░░░███  ░███░░░░░███  ░███    ░███    ░███    ░███      ░███ ░███░░█   
 ░███    ░███░░███     ███  ░███    ░███  ░███    ░███  ░███    ███     ░███    ░░███     ███  ░███ ░   █
 ███████████  ░░░███████░   █████   █████ █████   █████ ██████████      █████    ░░░███████░   ██████████
░░░░░░░░░░░     ░░░░░░░    ░░░░░   ░░░░░ ░░░░░   ░░░░░ ░░░░░░░░░░      ░░░░░       ░░░░░░░    ░░░░░░░░░░                                                                                                       
"""


SPLASH_TEXT = ("Bienvenido a BoardToe, un juego inspirado en el famoso tres en raya "
                "pero con la ventaja de poder jugarlo en tableros desde 3x3 hasta 8x8. " 
                "Además dispone de varios modos de juego diferentes como Jugador vs Jugador "
                "Jugador vs Maquina o Maquina vs Maquina. "
            )