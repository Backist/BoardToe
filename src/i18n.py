"""
Modulo que se encargar de la internacionalizacion del juego de manera muy básica.
"""

import importlib.resources
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
    

Languages = {}

with importlib.resources.open_text('src', 'translations.json') as file:
    content = file.read()
    # Aquí tendrías que implementar tu lógica para limpiar el JSONC si es necesario

    Languages = loads(content)    

AvailableLangs = list(Languages.keys())

def gphrase(lang: Language, context: Context, index: int):
    """
    Devuelve la frase correspondiente a la traducción del contexto y el índice en el diccinario de traducciones.
    """
    if lang not in AvailableLangs:
        raise ValueError("El idioma especificado no está disponible.")

    return Languages[lang][context][index]["phrase"]