"""
BoardToe helpers module.

This module contains a number of mathematical functions 
that operate on matrices mainly in different ways.

Refactored by Backist 2024.
Copyright 2022-2024 TheWisker-Backist.
"""

from copy import deepcopy
from src.mappings import GRID_TOKEN 


def matrix_view(matrix: list[list[int]]) -> None:
    """Simple and fast method to get a 2D view of a 2D matrix,
    intended for debugging purposes only"""
    
    v: str = "".join(f' {str(m)}' + '\n' for m in matrix)
    print("-"*len(matrix[0])*4+'\n', v, "-"*len(matrix[0])*4+'\n', sep="")


def replace_matrix(
    mtxs: list[list[list[int]]], 
    initial: list = None, 
    replacing: list = None, 
    reverse: bool = False
) -> list[list[list[int]]]:
    
    
    if initial is None and replacing is None:
        # Si ambos parámetros son nulos, reemplaza con el token vacío (GRID_TOKEN)
        initial, replacing = [GRID_TOKEN], [-1]
    else:
        initial += [GRID_TOKEN]
        replacing += [-1]

    if reverse:
        initial, replacing = replacing, initial

    def replace_value(vv):
        return replacing[initial.index(vv)] if vv in initial else vv

    return [
        [[replace_value(vv) for vv in row] for row in mtx] 
        for mtx in mtxs
    ] if len(mtxs) > 1 else [
        [replace_value(vv) for vv in row] for row in mtxs[0]
    ]



def rotate_matrix(matrix: list[list[int]], rts: int = 1, cw: bool = True) -> list[list[int]]:
    """
    ``Rota una matriz en sentido horario. La rotacion es de90 Grados predeterminadamente``
    - NOTE: ``4 rotaciones equivalen a 360 grados, es decir, a la posicion original.``

    ### Hasta x2 veces mas rapido que el metodo de rotacion de matrices de ``numpy``
    
    ### Ejemplo
    ```
    1. Original matrix:        2. Rotating 1 time (default rotation):

        Original               Rotated 90 degrees
        [0,0,1]                [0,1,0]
        [1,0,1]                [1,0,0]
        [0,1,1]                [1,1,1]
    ```
    """
    
    assert (
        isinstance(matrix, list) and len(matrix) >= 3
    ), "Param @matrix must be a list and depth <= 3."

    r = deepcopy(matrix)
    N = len(matrix)

    #If the rotation is clockwise, we swap the columns and rows
    for k in range(N):
        for kk in range(k):
            r[k][kk], r[kk][k] = r[kk][k], r[k][kk]

    if rts > 1:
        # recursion to rotate rts times
        return rotate_matrix(reverse_matrix(r, cw), rts-1)
    
    return reverse_matrix(r, cw) 


def rotate_index(inx: list[int, int], depth: int, cw: bool = False) -> list[int, int]:
    """
    Parameters:
        index: The index as [x, y]
        matrix_depth: The matrix length, 
        backwards: If it should rotate backwards or forwards
    Example:
        rotate_index([0,0], 3, False) -> [2,0]
    """
    
    r = [inx[0], inx[1]]
    r[1] = r[0]
    r[0] = depth-1-inx[1]
    return [r[1], r[0]] if cw else r


def reverse_matrix(matrix: list[list[int]], h: bool = True) -> list[list[int]]:
    """
    (es): Invierte una matriz horizontal o verticalmente.
    (en): Reverses a matrix horizontally or vertically.

    Horizontal reversion:
        [1,  1,  0] ------> [0,  1,  1]
        [1,  0,  0] ------> [0,  0,  1]
        [0,  0,  1] ------> [1,  0,  0]

    Vertical reversion:
        [1,  0,  0] ------> [0,  0,  1]
        [1,  1,  1] ------> [1,  1,  1]
        [0,  0,  1] ------> [1,  0,  0]
    """
    return [row[::-1] for row in matrix] if h else matrix[::-1]


def reverse_index(inx: list[int, int], dpth: int, h: bool = True) -> list[int, int]:
    """
    (es): Invierte un indice de una matriz invertida horizontal o verticalmente para conseguir su equivalente en la matriz original.\n
    (en): Reverses an index of a reversed matrix horizontal or vertically to get its equivalent index for the original matrix.\n

    Horizontal reversion:\n
                           Reversed -> Original\n
        [0,  1,  0] ------> (0,0)   ->  (0,2)\n
        [1,  0,  1] ------> (0,1)   ->  (0,1)\n
        [0,  0,  1] ------> (0,2)   ->  (0,0)\n

    Vertical reversion:\n
                           Reversed -> Original\n
        [0,  1,  0] ------> (0,0)   ->  (2,0)\n
        [1,  0,  1] ------> (1,0)   ->  (1,0)\n
        [0,  0,  1] ------> (2,0)   ->  (0,0)\n   
    """
    r = [inx[0], inx[1]] if h else [inx[1], inx[0]]
    r[1] = list(range(dpth-1, -1, -1))[r[1]]
    return r if h else [r[1], r[0]]


def win_check(matrix: list[list[int]], n: int) -> list[tuple[int, tuple[int]]]:
    "Function that returns a list with all the win positions for a player"
    return corner_check(matrix, n) + cross_check(matrix, n)


def corner_check(matrix: list[list[int]], n: int) -> list[list[tuple[int, list[int, int]]]]:
    "Function that returns a list with the horizontal and vertical win positions for a player"
    return row_check(matrix, n) + row_check(rotate_matrix(matrix), n, True)


def cross_check(matrix: list[list[int]], n: int) -> list[list[tuple[int, list[int, int]]]]:
    "Function that returns a list with both diagonal win position for a player"
    return [dgn_check(matrix, n), dgn_check(reverse_matrix(matrix), n, True)]


def row_check(matrix: list[list[int]], n: int, rt: bool = False) -> list[tuple[int, list[int]]] | None:
    "Function that returns a list with the horizontal win positions for a player"
    r = []
    for k,v in enumerate(matrix):
        if (len(set(v)) == 2 and all(x in set(v) for x in [-1, n])) or (len(set(v)) == 1 and v[0] == -1):
            rr: list = [
                rotate_index([k, kk], len(matrix)) if rt else [k, kk]
                for kk, vv in enumerate(v)
                if vv == -1
            ]
            r.append((v.count(-1), rr))
    return r or [None]


def dgn_check(matrix: list[list[int]], n: int, rt: bool = False) -> tuple[int, list[list[int, int]]] | None:
    "Function that returns a list with the first diagonal win position for a player"
    r = []
    dgn: list = [matrix[i][i] for i in range(len(matrix))]
    if (len(set(dgn)) == 2 and all(x in set(dgn) for x in [-1, n])) or (len(set(dgn)) == 1 and dgn[0] == -1):
        r.extend(
            reverse_index([k, k], len(matrix)) if rt else [k, k]
            for k, v in enumerate(dgn)
            if v == -1
        )
    return (dgn.count(-1), r) if r else None




if __name__ == '__main__':
    from src.utils import gen_model_mtx