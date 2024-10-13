"""
Este módulo se encarga de llevar el flujo de la entradas de datos del usuario.
En este caso, la única clase Logger contiene esencialmente "mensajes" que informan de errores,
pide entrada de coordenadas al usuario, entre otra información.
"""


from src import i18n
from src.termui.colors import Color
from src.mapping import EMOJIS
from typing import List


__all__: List[str] = ["Logger"]

class Logger:
    
    loggers: dict[str, list[str]] = {
        "errors":       [Color.BLUE, f"[{EMOJIS['GEARWHEEL']} ][{EMOJIS['MEGAPHONE']}] ",   Color.RED],
        "runtime":      [Color.BLUE, f"[{EMOJIS['MEGAPHONE']} ][{EMOJIS['EXCLAMATION']}] ", Color.YELLOW],
        "game":         [Color.BLUE, f"[{EMOJIS['CUP']} ][{EMOJIS['FIRST_MEDAL']}] ",       Color.CYAN],
        "draw":         [Color.LIGHT_GRAY, f"[{EMOJIS['TIE']} ][{EMOJIS['LOUDSPEAKER']}] ", Color.LIGHT_GRAY],
        "victory":      [Color.BLUE, f"[{EMOJIS['CUP']} ][{EMOJIS['FIRST_MEDAL']}] ",       Color.CYAN],
        "message":      [Color.BLUE, f"[{EMOJIS['GEARWHEEL']} ][{EMOJIS['LOUDSPEAKER']}] ", Color.WHITE],
        "question":     [Color.BLUE, f"[{EMOJIS['GEARWHEEL']} ][{EMOJIS['QUESTION']}] ",    Color.WHITE],
    }

    def __init__(self, lang: i18n.Language = i18n.Language.ENGLISH):
        
        if not hasattr(i18n.Language, lang):
            raise TypeError("Language not supported or its not available.")
        
        self.lang = lang
        
    @staticmethod 
    def available_loggers():
        return str(Logger.loggers)

    @staticmethod
    def get_phrase(context: i18n.Context, index: int, lang: i18n.Language = i18n.Language.ENGLISH) -> str:
        "Wrapper de gphrase."
        return i18n.Translator.gphrase(lang, context, index, needs_format=False)

    @staticmethod
    def phrase(p: str, logger: list[str]):
        assert logger in Logger.loggers.values(), "That logger is not in self.loggers dictionary"
        return f"\n{logger[0]+logger[1]}{logger[2]+p+Color.RESET}"

    #TODO: //////////////////////////////////   ADD METHODS  ////////////////////////////////
    
    def change_logger(self, logname: str, new: list[str]) -> None:
        if logname not in self.loggers:
            raise ValueError("That logger is not in the dictionary logger")
        self.new_logger(logname, new)
    
    def new_logger(self, logname: str, build: list[str]) -> None:
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
            raise ValueError("The first parameter must be an ASCII color code")
        elif build[1] in self.loggers.values():
            raise ValueError("The logger is registered in the logger dictionary with another logger name")
        elif build[1].count("[") < 1 or build[1].count("]") < 1:
            raise TypeError("The logger closure must have open-closed brackets to be a logger!")
        self.loggers[logname] = build
    
    def delete_logger(self, logname: str) -> None:
        assert isinstance(logname, str), "@logname must be a valid string!"
        del self.loggers[logname]

    def error(self, index: int = 3) -> str: return self.logger(i18n.Context.ERRORS, index, self.loggers["errors"])
    def token_question(self, index: int = 3) -> str: return self.logger(i18n.Context.GAME, index, self.loggers["question"])
    def victory(self, index: int = 4) -> str: return self.logger(i18n.Context.GAME, index, self.loggers["victory"])
    def draw(self, index: int = 5) -> str: return self.logger(i18n.Context.GAME, index, self.loggers["victory"])
    def info(self, index: int): return self.logger(i18n.Context.INFO, index, self.loggers["message"])
    def runtime(self, index: int = 3) -> str: return self.logger(i18n.Context.INFO, index, self.loggers["runtime"])
    
    def plquestion(self, index: int, pln: str, plc: Color) -> str: 
        return f"\n{self.loggers['question'][0]+self.loggers['question'][1]}[{plc+pln+self.loggers['question'][0]}] {self.loggers['question'][2]+self.get_phrase('game', index, self.lang)}"
    
    def logger(self, context: i18n.Context, index: int, logger: List[str]) -> str:
        assert isinstance(i18n.Context, context), "This context is not valid!!"

        if logger not in list(self.loggers.keys()):
            raise TypeError("This logger is not registered.")
        
        return f"\n{logger[0]+logger[1]}{logger[2]+self.get_phrase(context, index, self.lang)+Color.RESET}"
    

if __name__ == "__main__":

    def run_test():
        print(f"{Color.RED}[TEST] Testing Loggers ...{Color.RESET}")
        
        for lang, content in i18n.Languages.items():
            print(f"\n{Color.RED}[TEST] Testing {lang} ...{Color.RESET}\n\n")
            for level, lst in content.items():
                for phrase in lst:
                    print(Logger(lang).logger(level, lst.index(phrase), Logger.loggers[level]))
    
    run_test()
