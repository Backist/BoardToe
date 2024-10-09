

from src.consts import TOKENS
from typing import Union, List, Tuple, Dict
from functools import lru_cache
from os import system, name
    
def multiple_instcheck(vars: tuple, checks: Union[Tuple, None], manual_check: list = None, 
                       strict: bool = False) -> Union[bool, Tuple[bool, str]]:
     #! Hacer que el multiple_inscheck devuelva, en caso de strict=True, el valor que no cumple.
    """Function to simplicity the ``isinstance()`` checks.
    This function allow to check if n elements are instance of a type.
    
    >>> foo = 34
    >>> poo = '34'

    - Instead of:

    >>> if isinstace(foo, int) and isinstance(poo, int):
    >>>    ...

    - We do:

    >>> if not _multiple_instcheck((foo, poo), int):
    >>>     ...
    """
    if not manual_check and checks is None:
        raise AttributeError("Checks parameter must be passed if not 'manual_checks' is passed")

    if manual_check is None:
        return all(isinstance(e, checks) for e in vars)
    if isinstance(manual_check, (list, tuple)):
        return any(elem == mck for elem, mck in zip(vars, manual_check, strict=True))
    return all(elem == manual_check for elem in vars)



def get_key(rawDict: Dict, value, strict: bool = True) -> Union[Exception, None]:
    """Get a dictionary item through the key. 
    - If ``strict`` param is give (by deafult) an exception will be raised
    """
    if isinstance(rawDict, dict):
        if value not in list(rawDict.values()) and strict:
            raise ValueError(f"{repr(value)} is not in dictionary values (not in first layer)")  

        for k, v in rawDict.items():
            if v == value:
                return k

@lru_cache()
def multiple_replace(rawstr: str, reml: Tuple[Tuple[str, str]], count: int = -1):
    """Replacement optimized function."""
    assert isinstance(rawstr, str), "'@rawstr' parameter must be the string representation where the characters will be replaced"
    assert isinstance(reml, tuple), "'@reml' must be a tuple containing old-new values to be replaced"
    
    for i in reml:
        rawstr = rawstr.replace(i[0], i[1], count)
    return rawstr

def cls():
    return system("cls") if name == "nt" else system("clear")



if __name__ == "__main__":
    print(multiple_instcheck((34, '34'), (str), strict=True))