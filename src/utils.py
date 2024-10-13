"""
Funciones misceláneas, sin complicación. 
"""


from typing import Union, List, Tuple, Dict, Optional
from itertools import product
from random import randint
from functools import lru_cache
from src.tokens import TOKENS
    
def multiple_instcheck(vars: Tuple, checks: Optional[Tuple], manual_check: Optional[List] = None, 
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

def is_valid_token(token: str):
    return token in TOKENS.values()

def gen_model_mtx(size: int, method: str, active: int, random_alloc: bool = True) -> list:
    """
    Generates a square matrix of a specified size and populates it based on the given method and active value.

    This function initializes a matrix filled with zeros or ones, 
    depending on the `active` parameter and the `random_alloc` flag. 
    
    It then modifies the matrix according to the specified `method`, 
    which determines how the `active` value is placed within the matrix.

    Args:
        size (int): The size of the square matrix to be generated.
        method (str): The method used to populate the matrix. Options include "dwd", "h", "upd", and "v".
        active (int): The value to be placed in the matrix based on the specified method.
        random_alloc (bool, optional): If True, randomizes the allocation of any value that does not collision with value and avoids
        other ways to win. Defaults to True.

    Returns:
        list: A square matrix populated according to the specified parameters.
    """

    if not random_alloc and active == 0:
        # Segun quien gane se genera una matriz con todos los elementos contrarios al elemento ganador.
        matrix = [[1 for _ in range(size)] for _ in range(size)]
    else:
        matrix = [[0 for _ in range(size)] for _ in range(size)]

    if method == "dwd":
        for i, j in product(range(size), range(size)):
            if i == j:
                matrix[i][j] = active

    elif method == "h":
        for j in range(size):
            matrix[size // 2][j] = active  # Fila central

    elif method == "upd":
        for i, j in product(range(size), range(size)):
            if i + j == size - 1:
                matrix[i][j] = active

    elif method == "v":
        for i in range(size):
            matrix[i][size // 2] = active  # Columna central

    if random_alloc:
        for i in range(size):
            random_alloc = randint(0, size-1)
            if active != matrix[i][random_alloc]:
                matrix[i][random_alloc] = 1 if active == 0 else 0
                
    return matrix


if __name__ == "__main__":
    print(multiple_instcheck((34, '34'), (str), strict=True))