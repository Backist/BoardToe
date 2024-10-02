"""
BoardToe support module.

This module contains a number of mathematical functions 
that operate on matrices mainly in different ways.

Copyright 2022-2024 Backist.
"""
from copy import deepcopy
from consts import XTOKEN, OTOKEN, EMPTOKEN 


def matrix_view(matrix: list[list[int]]) -> None:
    """Simple and fast method to get a 2D view of a 2D matrix,
    intended for debugging purposes only"""
    v: str = "".join(f' {str(m)}' + '\n' for m in matrix)
    print("-"*len(matrix[0])*4+'\n', v, "-"*len(matrix[0])*4+'\n', sep="")
    return


def replace_matrix(mtxs: list[list[list]], _search: list = None, _replace: list = None, reverse: bool = False) -> list[list[list]]:
    if _search is None:
        _search = [EMPTOKEN, OTOKEN, XTOKEN]
    if _replace is None:
        _replace = [-1, 0, 1]
    if reverse:
        _search, _replace = _replace, _search
    r: list = []
    for mtx in mtxs:
        rr: list = []
        for v in mtx:
            rrr: list = [
                vv
                if vv not in _search and _search
                else _replace[_search.index(vv) if _search else 0]
                for vv in v
            ]
            rr.append(rrr)
        r.append(rr)
    return r if len(r) > 1 else r[0]


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
    ), f"Param @matrix must be a list and depth <= 3, no an {type(matrix).__name__}"
    assert isinstance(rts, int) or rts <= 4, f"You are trying to rotate the matrix more than 360 degrees wich equals to roating it {rts-4} times!!!"

    r: list = deepcopy(matrix)
    N: int = len(matrix)

    #We transpose the matrix clockwise or counterclockwise
    for k in range(N):
        for kk in range(k):
            r[k][kk], r[kk][k] = r[kk][k], r[k][kk]

    #Repeats the procedure for the number of times especified (rts)   
    if rts > 1:
        if rts == 4:
            print("You're rotating the matrix back to its original state")
        return rotate_matrix(reverse_matrix(r, cw), rts-1)
    return reverse_matrix(r, cw) #Here we interchange the columns vertically or horizonatlli depending on the direction of the rotation


def rotate_index(inx: list[int, int], depth: int, cw: bool = False) -> list[int, int]:
    """
    Parameters:
        index: The index as [x, y]
        matrix_depth: The matrix length, 
        backwards: If it should rotate backwards or forwards
    Example:
        rotate_index([0,0], 3, False) -> [2,0]
    """
    r: list = [inx[0], inx[1]]
    r[1] = r[0]
    r[0] = depth-1-inx[1]
    return [r[1], r[0]] if cw else r


def reverse_matrix(matrix: list[list], h: bool = True) -> list[list[int]]:
    """
    (es): Invierte una matriz horizontal o verticalmente.\n
    (en): Reverses a matrix horizontal or vertically.\n

    Horizontal reversion:\n
        [1,  1,  0] ------> [0,  1,  1]\n
        [1,  0,  0] ------> [0,  0,  1]\n
        [0,  0,  1] ------> [1,  0,  0]\n

    Vertical reversion:\n
        [1,  0,  0] ------> [0,  0,  1]\n
        [1,  1,  1] ------> [1,  1,  1]\n
        [0,  0,  1] ------> [1,  0,  0]\n
    """
    r: list = []
    if h:
        r.extend([item[kk] for kk in range(len(item) - 1, -1, -1)] for item in matrix)
    else:
        r.append([matrix[k] for k in range(len(matrix)-1, -1, -1)])
    return r


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
    r: list = [inx[0], inx[1]] if h else [inx[1], inx[0]]
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
    r: list = []
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
    r: list = []
    dgn: list = [matrix[i][i] for i in range(len(matrix))]
    if (len(set(dgn)) == 2 and all(x in set(dgn) for x in [-1, n])) or (len(set(dgn)) == 1 and dgn[0] == -1):
        r.extend(
            reverse_index([k, k], len(matrix)) if rt else [k, k]
            for k, v in enumerate(dgn)
            if v == -1
        )
    return (dgn.count(-1), r) if r else None





if __name__ == '__main__':
    models: dict[str, str] = {
        0: [
            [0, 1, -1],
            [0, 1, -1],
            [-1, -1, -1]
        ],
    }


"""
def transform2matrix(table: list[list], reps: list[tuple] = [("❌", 1), ("⭕", 0), ("➖", -1)], reverse_method: bool = False) -> list:
    
    ``Refactoriza una lista bimimensional o superior.``\n
    - Para hacer el proceso contrario, poner como ``True`` el parametro ``reverse_method``

    ## Parametros:

    - ``@table``: La lista bimimensional o superior.
    - ``@reps``: Lista conteniendo tuplas contiendo los valores antiguos a los valores nuevos.
    
    # er = [  
    #     ['❌', '➖', '❌'],
    #     ['⭕', '➖', '❌'],
    #     ['❌','❌','⭕'],
    # ]
    # print(transform2matrix(er))
    assert isinstance(table, list) and 3 <= len(table), f"Param @matrix must be a list and depth <= 3, no {type(table).__name__}"

    if reverse_method:
        for t in table:
            for _ in range(len(table)):
                for r in reps:
                    if t[_] == r[1]:
                        t[_] = r[0]
                    elif t[_] == r[1]:
                        t[_] = r[0]
                    elif t[_] == r[1]:
                        t[_] = r[0]
        return table
        
    for t in table:
        for _ in range(len(table)):
            for r in reps:
                if t[_] == r[0]:
                    t[_] = r[1]
                elif t[_] == r[0]:
                    t[_] = r[1]
                elif t[_] == r[0]:
                    t[_] = r[1]
    return table

if __name__ == "__main__":
    from dis import dis

    models: dict[str, str] = {

        1: [
            ["X", "-", "X"],
            ["0", "-", "0"],
            ["X", "0", "X"],

        ],
        2: [
            ['0', '-', '0', '0', '0'],
            ['-', '-', '-', '0', '0'],
            ['0', '-', '-', '0', '0'],
            ['0', '0', '-', '-', '-'],
            ['X', 'X', 'X', 'X', 'X']
        ],
        5: [
            ['0', '-', '0', '0', '0'],
            ['-', '-', '-', '0', 'X'],
            ['0', '-', '-', '0', 'X'],
            ['0', '0', '-', '-', 'X'],
            ['0', '0', '0', '0', '0']
        ],
        3: [
            [0,  0,   0, 0],
            [1, 1,  1, -1],
            [1,  1,   0,  0],
            [1, -1,  -1,  0]
        ],
        4: [
            ['X', '0', '-', 'X', '0', 'X', '0', '0'],
            ['-', '-', '0', 'X', 'X', '-', '0', '0'],
            ['X', '0', 'X', 'X', '-', '0', 'X', '-'],
            ['X', '0', '0', 'X', '0', '0', 'X', '0'],
            ['X', '0', '0', '0', 'X', 'X', '-', 'X'],
            ['X', '0', '-', 'X', '-', 'X', 'X', '-'],
            ['X', '0', '0', 'X', 'X', '0', 'X', '0'],
            ['0', '0', 'X', 'X', '0', 'X', '-', 'X']
        ],
        6: [
            [1, -1, 0],
            [0, -1, 0],
            [0, -1, 0]
        ],
        7: [
            [2, 3, 1],
            [1, 2, 3],
            [3, 1, 2],
        ]
} 

def rotate_matrix(matrix: list[list[int]], nofrots: int = 1, numpymethod: bool = False, returnm: bool = True, ) -> list[list[int]] | None:
    
    ``Rota una matriz en sentido horario. La rotacion es de  90 Grados predeterminadamente``
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
    
    assert isinstance(matrix, list) and 3 <= len(matrix), f"Param @matrix must be a list and depth <= 3, no {type(matrix).__name__}"
    assert isinstance(nofrots, int) or nofrots <= 4, f"You are trying to rotate the matrix 360 degrees (Original position)!!"

    if nofrots > 1:
        for _ in range(nofrots):
            matrix = rotate_matrix(matrix, nofrots, numpymethod, returnm)
        return matrix

    if numpymethod:
        m = np.array(matrix, dtype=int)
        np.rot90(m, 1, (-1, 0))
        return m if returnm else None

    N = len(matrix)

    #transponemos la matriz hacia las abujas del reloj (90 Grados)
    for i in range(N):
        for j in range(i):
            temp = matrix[i][j]
            matrix[i][j] = matrix[j][i]
            matrix[j][i] = temp
        
    #aqui cambias las columnas (columnas de intercambio)
    for i in range(N):
        for j in range(N // 2):
            temp = matrix[i][j]
            matrix[i][j] = matrix[i][N - j - 1]
            matrix[i][N - j - 1] = temp
    
    return matrix if returnm else None
    
    
def hcheck(matrix: list[list[int]]) -> list[list[int | tuple[int, int]]] | list:
    ``Metodo general usado para comprobar si algun jugador esta a un movimiento de hacer una sucesion horizontal.``
    #### NOTE! Este metodo se puede aplicar para comprobar una sucesion en cualquier direccion, tan solo rotando la matriz.
    
    ### Ejemplo:
    >>>    [0,1,0],
    >>>    [1,0,0],
    >>>    [1,1,-1]
    
    - En este caso la lista de indice ``2`` (``[1,1,-1]``) es una sucesion horizontal de los mismos elementos menos 1 elemento que esta vacio.
    - En ese caso se devuelve la ficha que gana y la posicion que falta para completar esa sucesion horizontal -> ``(1, (2,2))``

    assert isinstance(matrix, list) or not all(isinstance(e, list) for e in matrix) or not matrix, "@index param must be list containing tuples that contain integers"

    results: list = []

    for i, subarray in enumerate(matrix):

        if all(elem == subarray[0] for elem in subarray) or not -1 in subarray or subarray.count(-1) > 1:
            continue  
        #* sabemos que las listas que tenemos solo tienen un -1
        empty_index: int = subarray.index(-1)
        if len(set(subarray)) == 2:     
            results.append([subarray[empty_index-1], (i, empty_index)])
    return results


    #!HAY QUE ARREGLARLO IMPLEMENTANDO EL REVERSE MATRIX
    def dcheck(matrix: list[tuple[int]]) -> list[list[int | tuple[int, int]]] | list:
    
    ``Metodo usado para comprobar si algun jugador esta a un movimiento de hacer una sucesion diagonal.``

    ### Ejemplo:
    >>>    [0,1,1],
    >>>    [1,0,0],
    >>>    [1,-1,-1]

    - En este caso hay una diagonal desde el indice ``[0,0]`` hasta ``[-1][-1]``
    - En ese caso se devuelve la ficha que gana y la posicion que falta para completar esa sucesion diagonal -> ``(0, (2,2))``
    

    r = []  #? para almacenar los datos finales
    templist = [matrix[i][i] for i in range(len(matrix))]
    
    if templist.count(-1) == 1 and len(set(templist)) == 2:
        empty_index = templist.index(-1)
        r.append([templist[empty_index-1], (empty_index, empty_index)])

    templist.clear()

    for a,i in zip(range(len(matrix)), range(len(matrix)-1, -1, -1), strict=True):
        templist.append(matrix[a][i]) 
        if templist.count(-1) == 2 or len(set(templist)) > 2:
            r.pop()
            break
        elif templist[-1] == -1 and templist.count(-1) == 1 and len(set(templist)) == 2:
            r.append([templist[templist.index(-1)-1], (a, i)])
    return r

    def check_win(matrix: list[list[int]], player: dict[str,]) -> list[list]: 
    Comprueba y devuelve que jugadores pueden ganar colocando una sola ficha
    - NOTE: La funcion puede devolver una lista vacia si ningun jugador esta a un movimiento de ganar
    - NOTE 2: Si los dos jugadores comparten una posicion, se muestran las dos posiciones, no una.

    wins: list = []

    if not player["token"] in ["X", "0"]:
        raise TypeError(f"Player token must be X or 0, not {repr(player['token'])}")

    pltoken = 1 if player["token"] == "X" else 0

    deeplist = deepcopy(matrix)      #? memoize list, to create a new list in a new memory object
    rotmatx = rotate_matrix(deeplist)

    if hcheck(matrix):
        wins.extend([p for p in hcheck(matrix) if p[0] == pltoken])
    if hcheck(rotmatx):
        wins.extend(rotate_index([p for p in hcheck(rotmatx) if p[0] == pltoken], len(rotmatx)))  #* Vertical check (Rotate matrix)
    if dcheck(matrix):
        wins.extend([p for p in dcheck(matrix) if p[0] == pltoken])
    
    return wins
"""