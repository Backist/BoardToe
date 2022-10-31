"""Main core module"""


def pview(matrix: list[list[int]]) -> None:
    "Easy, rapid method to get a pretty view of the matrix"
    print("-"*len(matrix)*4)
    for i in matrix:
        print(f"{i}")
    print("-"*len(matrix)*4)
    return


def transform2matrix(table: list[list[int]], reverse_method: bool = None) -> list:
    """
    ``Transforma una tabla bidimensional o superior con caracteres,
    a una matriz de la misma profundidad con valores numericos o viceversa.``\n
    - Para pasar de una matriz binaria a una de caracteres, poner como ``True`` el parametro ``reverse_method``
    """
    assert isinstance(table, list) and 3 <= len(table), f"Param @matrix must be a list and depth <= 3, no {type(table).__name__}"

    if reverse_method is not None:
        for i in range(len(table)):
            for _ in range(len(table)):
                if table[i][_] == -1:
                    table[i][_] = "-"
                elif table[i][_] == 0:
                    table[i][_] = "0"
                elif table[i][_] == 1:
                    table[i][_] = "X"
        return table
        
    for i in range(len(table)):
        for _ in range(len(table)):
            if table[i][_] == "-":
                table[i][_] = -1
            elif table[i][_] == "0":
                table[i][_] = 0
            elif table[i][_] == "X":
                table[i][_] = 1
    return table


def rotate_matrix(matrix: list[list[int]], nofrots: int = 1) -> list[list[int]]:
    """
    ``Rota una matriz en sentido horario. La rotacion es de  90 Grados predeterminadamente``
    - NOTE: ``4 rotaciones equivalen a 360 grados, es decir, a la posicion original.``
    
    ### Ejemplo
    ```
    1. Original matrix:        2. Rotating 1 time (default rotation):

        Original               Rotated 90 degrees
        [0,0,1]                [0,1,0]
        [1,0,1]                [1,0,0]
        [0,1,1]                [1,1,1]
    ```
    """
    assert isinstance(matrix, list) and 3 <= len(matrix), f"Param @matrix must be a list and depth <= 3, no {type(matrix).__name__}"
    assert isinstance(nofrots, int) or nofrots <= 4, f"You are trying to rotate the matrix 360 degrees (Original position)!!"

    if nofrots > 1:
        for _ in range(nofrots):
            matrix = rotate_matrix(matrix)
        return matrix

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
    
    return matrix


def hcheck(matrix: list[list[int]]) -> list:
    """``Metodo general usado para comprobar si algun jugador esta a un movimiento de hacer una sucesion horizontal.``
    #### NOTE! Este metodo se puede aplicar para comprobar una sucesion en cualquier direccion, tan solo rotando la matriz.
    
    ### Ejemplo:
    >>>    [0,1,0],
    >>>    [1,0,0],
    >>>    [1,1,-1]
    
    - En este caso la lista de indice ``2`` (``[1,1,-1]``) es una sucesion horizontal de los mismos elementos menos 1 elemento que esta vacio.
    - En ese caso se devuelve la ficha que gana y la posicion que falta para completar esa sucesion horizontal -> ``(1, (2,2))``
    """
    assert isinstance(matrix, list) or not all(isinstance(e, list) for e in matrix) or not matrix, "@index param must be list containing tuples that contain integers"

    results: list = []

    for i, subarray in enumerate(matrix):

        if all(elem == subarray[0] for elem in subarray) or not -1 in subarray or subarray.count(-1) > 1:
            #? si los elementos son iguales (todo 1, 0, o -1), o hay mas de un -1, que continue 
            continue  
        #* sabemos que las listas que tenemos solo tienen un -1
        empty_index: int = subarray.index(-1)
        if len(set(subarray)) == 2:     #? la estructura set no permite elementos iguales, si existen dos (misma ficha y el -1) es que es True
            results.append((subarray[i if subarray[i] != -1 else i-1], (i, empty_index))) #* (jugador que gana, [posicion donde puede ganar])
    return results


def dcheck(matrix):
    """``Metodo usado para comprobar si algun jugador esta a un movimiento de hacer una sucesion diagonal.``

    ### Ejemplo:
    >>>    [0,1,1],
    >>>    [1,0,0],
    >>>    [1,-1,-1]

    - En este caso hay una diagonal desde el indice ``[0,0]`` hasta ``[-1][-1]``
    - En ese caso se devuelve la ficha que gana y la posicion que falta para completar esa sucesion diagonal -> ``(0, (2,2))``
    """
    r = []

    if len(matrix) % 2 != 0:
        cm = matrix[len(matrix) // 2][len(matrix) // 2]

        if cm == -1:
            return []
        
        else:

            d = []
            for i in range(len(matrix)):
                d.append(matrix[i][i])        
                if len(set(d)) == 2:
                    r.append((d[0] if d[0] != -1 else d[-1], (i, d.index(-1))))     #! esta MAL

            # for i,s in zip(range(len(matrix)-1, -1, -1), range(len(matrix)), strict=True):
            #     d.append(matrix[i][i])
            #     if len(set(d)) == 2:
            #         r.append((d[0] if d[0] != -1 else d[-1], (i, d.index(-1))))

            return r

            # elif matrix[0][-1] == matrix[-1][0] and matrix[0][-1] != -1:
            #     for i,s in zip(range(len(matrix)-1, 1, -1), range(1, len(matrix)-1), strict=True):
            #         if matrix[i-1][s] != -1:
            #             break
            #         elif i == len(matrix)-2 and matrix[i][i] == -1:
                        # r.append((matrix[i][i], (i, i)))

    return []


def rotate_index(index: list[tuple[int, int]], depth: int) -> list[tuple[int, int]]:
    """
    Rota un indice o una lista de indices correspondientes de una matriz rotada 90 grados para su equivalencia en su matriz original.\n

    - ``@index`` -> El indice o lista de indices.
    - ``@depth`` -> La longitud de la matrix original.
    
    ### Ejemplo:

    ```
    Matriz rotada:      Si cogemos la primera fila vertical [0, 1, -1], los indices de sus elementos en la original son:

                            Rotada   Original
    [0,  1, -1]             (0,0) -> (0,2)
    [1,  0,  1]             (1,0) -> (0,1)
    [-1, 0,  1]             (2,0) -> (0,0)                 
    ```
    """
    assert isinstance(index, list) or not all(isinstance(e, list) for e in index) or not index, "@index param must be list containing tuples that contain integers"

    if len(index) < 1:
        return None
    
    #! Valorar si pasar solo los indices o la lista con el jugador incluido
    index = [[i[0], list(i[1])] for i in index]
    for i in index:
        temp = i[1][1]
        i[1][1] = i[1][0]
        i[1][0] = depth-1-temp
        index[index.index(i)] = i
    return [(i[0], tuple(i[1])) for i in index]


def check_adjacent(matrix: list[list[int]], player: int) -> list[tuple[int, tuple[int, int]]]: #[(x,y), ...]
    "Function that returns a list with the adjacent positions to each player"
    assert isinstance(matrix, list) and 3 <= len(matrix), f"Param @matrix must be a list and depth <= 3, no {type(matrix).__name__}"
    #TERMINALO PERRACO


def check_win(matrix: list[list[int]]) -> list[tuple[int,int]]:
    """Comprueba y devuelve que jugadores pueden ganar colocando una sola ficha
    - NOTE: La funcion puede devolver una lista vacia si ningun jugador esta a un movimiento de ganar
    - NOTE 2: Si los dos jugadores comparten una posicion, se muestran las dos posiciones, no una.
    """
    results: list = []
    
    results.extend(hcheck(matrix)) #* Horizontal check
    results.extend(rotate_index([e for e in hcheck(rotate_matrix(matrix))], len(matrix))) #* Vertical check (Rotate matrix)
        
    return results
  

if __name__ == "__main__":
    raw_matrix = [
        ["X", "-", "X"],
        ["0", "-", "X"],
        ["-", "0", "X"],

    ]

    er3 = [
        ['X', '0', '-', 'X', '0'],
        ['X', '-', 'X', 'X', 'X'],
        ['X', '0', '0', 'X', '-'],
        ['X', '0', 'X', 'X', 'X'],
        ['-', '0', '0', '-', '0']
    ]

    matrix1 = transform2matrix(raw_matrix)
    matrix2 = transform2matrix(er3)
    # print(rotate_matrix(bin_matrix))

    # print(check_enemy_win(matrix1))
    print(dcheck(matrix1))
   
    """
    Vamos a ver, no puedo acabar el bot sin las siguientes funciones: 
        · check_win(player) Checkea si el jugador pasado de argumento (0 o 1) esta a un movimiento de ganar horizontal, vertical y diagonalmente.
        Devuelve una tupla o lista con todas las posiciones con las que dicho jugador puede ganar y si no hay la devuleve vacia.
        Ej: return [(x,y), ...]
        (De segundas): Para mayor comprobacion habria que devolver un booleano que especifique cuanda hay mas de dos posibles jugadas ganadoras si estan relacionadas, si es true es una victoria absoluta, si es false aun puedes perder.
        Ej: return [(x,y), ...], bool_de_relacion
        · check_adjacent(player) Checkea todas las posiciones en la tabla donde el jugador pasado de parametro pueda colocar una ficha adyacente a otra suya.
        Devuelve una tupla o lista con todas las posiciones con las que dicho jugador puede poner adyacentes especificando para cada posicion cuantas fichas adyacentes suyas tiene, cuantas adyacentes eneigas tiene y cuantas vacias adyacentes tiene y si no hay la devuleve vacia.
        Ej: return [((adyacentes_aliadas: int, adyacentes_enemigas: int, adyacentes_vacias: int), (x,y)),...]

    Con estas dos simples funciones bastaria pero para mayor complejidad metele la siguiente funcion:
        · check_prediction(player) Checkea el proximo movimiento del jugador pasado segun la propia forma del bot de calcular sus movimientos.
        return AunNoSeQueDevuelve
    """