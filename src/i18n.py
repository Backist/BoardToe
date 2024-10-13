"""
Modulo que se encargar de la internacionalizacion del juego de manera muy básica.
"""

import importlib.resources
from typing import List, Tuple, Union, Dict, Optional
from json import loads

__all__ = ["Languages", "Language", "Context", "AvailableLangs"]

class Language:
    "Clase que ayuda a obtener el nombre del idioma."
    SPANISH = "SPANISH"
    CATALAN = "CATALAN"
    EUSKERA = "EUSKERA"
    RUSSIAN = "RUSO"
    FRENCH = "FRANCES"
    GERMAN = "ALEMAN"
    JAPANESE = "JAPANESE"
    SIMPLIFIED_CHINESE = "SIMPLIFIED_CHINESE"
    TRADITIONAL_CHINESE = "TRADITIONAL_CHINESE"
    ITALIAN = "ITALIAN"
    
class Context:
    "Clase que ayuda a obtener el nombre del contexto."
    GAME = "GAME"
    ERRORS = "ERRORS"
    INFO = "INFO"
    MISC = "MISC"
    SPLASH = "SPLASH"


def _load_translations() -> Dict[str, Dict[str, Dict[str, Dict[str, Dict]]]]:
    with importlib.resources.read_text('src', 'translations.json') as file:
        return loads(file)


class Translator:
    Languages = _load_translations()
    AvailableLangs = list(Languages.keys())

    @classmethod
    def update(cls, translations: Dict[str, Tuple[str, bool]], 
               context: str, custom_idx: Optional[int] = None):
        
        if not hasattr(Context, context):
            raise ValueError("This context is not available.")
        elif len(translations) != len(cls.AvailableLangs):
            raise ValueError("When updating translations, we need to pass all the available languages.")
    
        Tmap = cls.Languages

        # Procesamos cada traducción por idioma
        for lang, (phrase, format) in translations.items():
            
            if lang not in cls.AvailableLangs:
                raise ValueError("This language is not available.")
            
            context_phrases = Tmap[lang][context]
            length = len(context_phrases)
            
            if custom_idx:
                if custom_idx > length + 1:
                    raise ValueError(f"custom_idx ({custom_idx}) is greater than the number of existing items ({length + 1}).")
                
                # Mover elementos hacia abajo y hacer espacio para la nueva frase
                for i in range(length, custom_idx - 1, -1):
                    context_phrases[str(i + 1)] = context_phrases[str(i)]

                context_phrases[str(custom_idx)] = {"phrase": phrase, "format": format}
            else:
                # append to the end
                context_phrases[str(length + 1)] = {"phrase": phrase, "format": format}
        
        # Actualizamos las translations
        Translator._update_translation_file(Tmap)

    
    @staticmethod 
    def gphrase(lang: Language, context: Context, index: int, needs_format: bool = True):
        """
        Devuelve la frase correspondiente a la traducción del contexto y el índice en el diccinario de traducciones.
        """
        if lang not in Translator.AvailableLangs:
            raise ValueError("El idioma especificado no está disponible.")
        
        if needs_format:
            return Languages[lang][context][index]["phrase"], Languages[lang][context][index]["format"]
        else:
            return Languages[lang][context][index]["phrase"] 

    @staticmethod
    def _update_translation_file(translations_map):
        """Guardar el diccionario de traducciones actualizado en el archivo JSON."""
        with open('src/translations.json', 'w', encoding='utf-8') as file:
            file.write(dumps(translations_map, ensure_ascii=False, indent=4))



if __name__ == "__main__":
    from json import dumps
    from copy import deepcopy
    
    test = deepcopy(Translator.Languages)
    
    new_translation = {
        "ENGLISH": ("You need to restart the system.", False),
        "SPANISH": ("Necesitas reiniciar el sistema.", False),
        "EUSKERA": ("Sistema berrabiarazi behar duzu.", False),
        "CHINESE_SIMPLIFIED": ("您需要重新启动系统。", False),
        "CHINESE_TRADITIONAL": ("您需要重新啟動系統。", False),
        "FRENCH": ("Vous devez redémarrer le système.", False),
        "RUSSIAN": ("Вам нужно перезагрузить систему.", False),
        "ITALIAN": ("È necessario riavviare il sistema.", False),
        "CATALAN": ("Has de reiniciar el sistema.", False),
        "GERMAN": ("Sie müssen das System neu starten.", False)
    }

    Translator.update(new_translation, context=Context.ERRORS, custom_idx=3)
    print(dumps(test, indent=4))
        
        
    