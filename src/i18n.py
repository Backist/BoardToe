

import importlib.resources
from json import loads

__all__ = ["Language", "Languages_", "AvialableLangs"]


class Languages_:
    SPANISH = "SPANISH"
    ENGLISH = "ENGLISH"
    GERMAN = "GERMAN"
    ITALIAN = "ITALIAN"
    RUSSIAN = "RUSSIAN"
    FRENCH = "FRENCH"
    PORTUGUESE = "PORTUGUESE"
    JAPANESE = "JAPANESE"
    CHINESE = "CHINESE"
   
Language = {}   
 
with importlib.resources.open_text('src', 'translations.json') as file:
    content = file.read()
    # Aquí tendrías que implementar tu lógica para limpiar el JSONC si es necesario

    Language = loads(content)    
    

AvailableLangs = list(Language.keys())
