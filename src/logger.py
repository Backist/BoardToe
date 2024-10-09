
import unicodedata

from src import i18n
from src.consts import EMOJIS, EmojiID
from pybeaut import Col, Banner, Cursor

__all__: list[str] = ["Logger"]


# "gearwheel": " ⚙️ ",
# "megaphone": "📢",
# "lock": "🔒",
# "stop_signal": "⛔️",
# "exclamation": "❕",
# "loudspeaker": "🔊",
# "tie": "🤝",
# "robotic_arm": "🦾",
# "first_medal": "🥇",
# "cup": "🏆",
# "robot": "🤖",
# "magnifying_glass": "🔍"
# "question": "❔"


class Logger:
    
    loggers: dict[str, list[str, str]] = {
        "errors":       [Col.blue, f"[{EMOJIS[EmojiID.GEARWHEEL]} ][{EMOJIS[EmojiID.MEGAPHONE]}] ",   Col.red],
        "runtime":      [Col.blue, f"[{EMOJIS[EmojiID.MEGAPHONE]} ][{EMOJIS[EmojiID.EXCLAMATION]}] ", Col.yellow],
        "game":         [Col.blue, f"[{EMOJIS[EmojiID.CUP]} ][{EMOJIS[EmojiID.FIRST_MEDAL]}] ",       Col.cyan],
        "draw":         [Col.gray, f"[{EMOJIS[EmojiID.TIE]} ][{EMOJIS[EmojiID.LOUDSPEAKER]}] ",       Col.gray],
        "victory":      [Col.blue, f"[{EMOJIS[EmojiID.CUP]} ][{EMOJIS[EmojiID.FIRST_MEDAL]}] ",       Col.cyan],
        "message":      [Col.blue, f"[{EMOJIS[EmojiID.GEARWHEEL]} ][{EMOJIS[EmojiID.LOUDSPEAKER]}] ", Col.white],
        "question":     [Col.blue, f"[{EMOJIS[EmojiID.GEARWHEEL]} ][{EMOJIS[EmojiID.QUESTION]}] ",    Col.white],
    }

    def __init__(self, lang: i18n.Languages = i18n.Languages.ENGLISH):
        self.lang = lang
        
    @staticmethod 
    def available_loggers():
        return str(Logger.loggers)

    @staticmethod
    def _get_phrase(level: str, index: int, lang: i18n.Languages = i18n.Languages.ENGLISH) -> str:
        "Retorna la frase del indice del nivel e idioma pasado."
        return i18n.langs[lang][level.lower()][index]

    @staticmethod
    def phrase(p: str, logger: list[str]):
        assert logger in Logger.loggers.values(), "That logger is not in self.loggers dictionary"
        return f"\n{logger[0]+logger[1]}{logger[2]+p+Col.reset}"


    #TODO: //////////////////////////////////   ADD METHODS  ////////////////////////////////
    
    def change_logger(self, logname: str, new: list[str]) -> None:
        if logname not in self.loggers:
            raise ValueError("That logger is not in the dictionary logger")
        self.new_logger(logname, new)
    
    def new_logger(self, logname: str, build: list[str]) -> None:
        # sourcery skip: raise-specific-error
        """Crea un nuevo logger dentro del diccionario self.loggers si no existe.
        
        ## Parametros:
        - logname: El nombre del logger
        - build: Lista que debe contener el color de prefijo, el logger, y el color final        
        """
        assert isinstance(logname, str), "@logname must be a valid string!"
        assert isinstance(build, list) and len(build) == 3, "Invalid build. @build is major than 3 elems or @build is not a list"

        if logname in self.loggers:
            raise ValueError("That logger already exists in the self.loggers dictionary")
        elif not isinstance(build[0], list) and not build[0].startswith("\\x"):
            raise ValueError("The fisrt parameter must be a ascii color code")
        elif build[1] in self.loggers.values():
            raise ValueError("The logger is registred in the logger dictionary with another logger name")
        elif build[1].count("[") < 1 or build[1].count("]") < 1:
            raise Exception("The logger clausure must be a open-closed brackets to be a logger!")
        self.loggers[logname] = build
    
    def delete_logger(self, logname: str) -> None:
        assert isinstance(logname, str), "@logname must be a valid string!"
        del self.loggers[logname]

    
    #TODO: //////////////////////////////////   self.LOGGERS  ////////////////////////////////
    #* Podria hacer un solo metodo que tambien pase el tipo de frase en vez de repetir, pero quiero que puedas acceder como si de un logger se tratara
    #* Logger.error(<index>) en vez de Logger.logger("errors", 1)

    def error(self, index: int) -> str:
        return self.logger("errors", index, self.loggers["errors"])
        
    def question(self, index: int) -> str:
        return self.logger("game", index, self.loggers["question"])
    
    def plquestion(self, index: int, pln: str, plc: Col) -> str:
        return f"\n{self.loggers['question'][0]+self.loggers['question'][1]}[{plc+pln+self.loggers['question'][0]}] {self.loggers['question'][2]+self._get_phrase('game', index, self.lang)}"

    def victory(self, index: int) -> str:
        "Se devuelve un mensaje logger con un mensaje de victoria"
        return self.logger("game", index, self.loggers["victory"])
    
    def draw(self, index: int) -> str:
        "Se devuelve un mensaje logger con un mensaje de empate"
        return self.logger("game", index, self.loggers["victory"])
    
    def message(self, index: int):
        return self.logger("game", index, self.loggers["message"])

    def runtime(self, index: int) -> str:
        "Se devuelve un mensaje logger con un mensaje relacionado con el flujo del juego"
        return self.logger("runtime", index, self.loggers["runtime"])

    def logger(self, level: str, index: int, logger: list[str]) -> str:
        assert isinstance(level, str), "This is not a valid level!"
        assert isinstance(index, int), "Index must be a integer!!"
        if logger not in self.loggers.values():
            raise TypeError("@logger param must be a valid logger type.")
        return f"\n{logger[0]+logger[1]}{logger[2]+self._get_phrase(level, index, self.lang)+Col.reset}"
    

if __name__ == "__main__":

    def crear_caja(frase):
        # Determinar el tamaño de la caja
        longitud = len(frase)+4  # Se suman 2 para los espacios en blanco

        return (
            '╭' + '─' * (longitud) + '╮' + '\n'
            f'│  {frase}  │' + '\n'
            '╰' + '─' * (longitud) + '╯' + '\n'
        )


    def calculate_width(text):
        total_width = 0
        for char in text:
            # Obtener la categoría del carácter
            if unicodedata.category(char) in ('So', 'Cn', 'Lo', 'Lu', 'Ll', 'Lt', 'Lm', 'Lo'):
                # Consideramos caracteres de ancho completo (ej: japonés, chino)
                total_width += 2 if unicodedata.combining(char) == 0 else 1
            else:
                total_width += 1  # Asumimos ancho medio para otros caracteres
        return total_width

    def run_test():
        print(f"{Col.red}[TEST] Testing Loggers ...{Col.reset}")
        
        for lang, content in i18n.langs.items():
            print(f"\n{Col.red}[TEST] Testing {lang} ...{Col.reset}\n\n")
            for level, lst in content.items():
                for phrase in lst:
                    print(f"{Col.red}{crear_caja(Logger(lang).logger(level, lst.index(phrase), Logger.loggers[level]))}{Col.reset}")
    run_test()