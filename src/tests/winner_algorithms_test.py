"""
Benchmark and test performance of win check algorithm.

Copyright Backist 2022-2024 under license GPL 3.0.
"""
from random import randint
from pybeaut import Col
import itertools

# %%%%%%%%%%%%%%%%%%%%%%%%%%%    Win algorithms   %%%%%%%%%%%%%%%%%%%%%%%%%%%
def check_win(board) -> bool:
    """
    Verifica si se ha ganado la partida revisando:
    - Líneas horizontales.
    - Líneas verticales.
    - Diagonales en tablas de tamaño impar.
    - Diagonales en tablas de tamaño par.
    
    Returns:
        bool: True si se ha encontrado una condición de victoria, False en caso contrario.
    """
    if _check_horizontal_win(board):
        return True
    if _check_vertical_win(board):
        return True
    if len(board) % 2 == 0 and _check_diagonal_even_board_win(board):
        return True
    return bool(_check_diagonal_odd_board_win(board))

def _check_horizontal_win(board) -> bool:
    """
    Verifica si alguna fila tiene todos los elementos iguales y no contiene valores vacíos (-1).
    
    Returns:
        bool: True si se detecta una victoria en una fila, False en caso contrario.
    """
    for row in board:
        if -1 in row:
            continue  # Si la fila contiene un espacio vacío, no es ganadora.
        if len(set(row)) == 1:  # Si todos los elementos en la fila son iguales.
            return True
    return False

def _check_vertical_win(board) -> bool:
    """
    Verifica si alguna columna tiene todos los elementos iguales y no contiene valores vacíos (-1).
    
    Returns:
        bool: True si se detecta una victoria en una columna, False en caso contrario.
    """
    for i in range(len(board)):
        if (board[0][i] == -1 or board[-1][i] == -1) or (board[0][i] != board[-1][i]):
            continue  # Si las esquinas de la columna no coinciden, no es ganadora.
        
        checks = [board[j][i] for j in range(1, len(board)-1)]
        if all(elem == board[0][i] for elem in checks):
            return True
    return False

def _check_diagonal_odd_board_win(board) -> bool:
    """
    Verifica si existe una victoria diagonal en tablas de tamaño impar.
    
    Returns:
        bool: True si se detecta una victoria diagonal, False en caso contrario.
    """
    center = len(board) // 2
    token = board[center][center]  # El valor central de la tabla impar.

    if token == -1:
        return False  # Si el centro está vacío, no puede haber una diagonal ganadora.

    # Diagonal descendente (\)
    if board[0][0] == board[-1][-1] and board[0][0] == token:
        for i in range(1, len(board)-1):
            if board[i][i] != token:
                break
            elif i == len(board)-2:
                return True

    # Diagonal ascendente (/)
    if board[0][-1] == board[-1][0] and board[0][-1] == token:
        for i, s in zip(range(len(board)-1, 1, -1), range(1, len(board)-1)):
            if board[i-1][s] != token:
                break
            elif s == len(board)-2:
                return True

    return False

def _check_diagonal_even_board_win(board) -> bool:
    """
    Verifica si existe una victoria diagonal en tablas de tamaño par.
    
    Returns:
        bool: True si se detecta una victoria diagonal, False en caso contrario.
    """
    if board[0][0] == -1 or board[0][-1] == -1:
        return False  # Si alguna de las esquinas está vacía, no puede haber una diagonal ganadora.

    # Diagonal descendente (\)
    if board[0][0] == board[-1][-1]:
        for i in range(1, len(board)-1):
            if board[i][i] != board[0][0]:
                break
            elif i == len(board)-2:
                return True

    # Diagonal ascendente (/)
    if board[0][-1] == board[-1][0]:
        for i, s in zip(range(len(board)-1, 1), range(1, len(board)-1)):
            if board[i][s] != board[0][-1]:
                break
            elif s == len(board)-2:
                return True

    return False

def check_draw(board) -> bool:
    """
    Verifica si ha habido un empate segun la posicion de los tokens de cada jugador. 
    Por ahora solo verifica que ha habido un empate cuando en la tabla no hay mas posiciones libres y nadie a ganado
    """
    
    for i in range(len(board)):
        if any(elem == -1 for elem in board[i]):
            break
        if i == len(board)-1:
            return True

    empty_locs = sum(
        board[i][s] == -1
        for i, s in zip(range(len(board)), range(0, len(board), -1))
    )
    return False



# %%%%%%%%%%%%%%%%%%%%%%%%%%%    Test cases   %%%%%%%%%%%%%%%%%%%%%%%%%%%

def genmtx(size: int, method: str, active: int, random_alloc: bool = True) -> list:
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
        for i, j in itertools.product(range(size), range(size)):
            if i == j:
                matrix[i][j] = active

    elif method == "h":
        for j in range(size):
            matrix[size // 2][j] = active  # Fila central

    elif method == "upd":
        for i, j in itertools.product(range(size), range(size)):
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

def print_matrix(matrix):
    for row in matrix:
        print(" | ".join(str(cell) for cell in row))
        print("_" * (len(row) * 4 - 1))  # Dibuja una línea entre las filas
        
test_cases = {
    "3x3": {
        "1": {
            "upwards_diagonal": genmtx(3, "upd", 1),
            "downwards_diagonal": genmtx(3, "dwd", 1),
            "vertical": genmtx(3, "v", 1),
            "horizontal": genmtx(3, "h", 1),
        },
        "0": {
            "upwards_diagonal": genmtx(3, "upd", 0),
            "downwards_diagonal": genmtx(3, "dwd", 0),
            "vertical": genmtx(3, "v", 0),
            "horizontal": genmtx(3, "h", 0),
        }
    },
    "4x4": {
        "1": {
            "upwards_diagonal": genmtx(4, "upd", 1),
            "downwards_diagonal": genmtx(4, "dwd", 1),
            "vertical": genmtx(4, "v", 1),
            "horizontal": genmtx(4, "h", 1),
        },
        "0": {
            "upwards_diagonal": genmtx(4, "upd", 0),
            "downwards_diagonal": genmtx(4, "dwd", 0),
            "vertical": genmtx(4, "v", 0),
            "horizontal": genmtx(4, "h", 0),
        }
    },
    "5x5": {
        "1": {
            "upwards_diagonal": genmtx(5, "upd", 1),
            "downwards_diagonal": genmtx(5, "dwd", 1),
            "vertical": genmtx(5, "v", 1),
            "horizontal": genmtx(5, "h", 1),
        },
        "0": {
            "upwards_diagonal": genmtx(5, "upd", 0),
            "downwards_diagonal": genmtx(5, "dwd", 0),
            "vertical": genmtx(5,"v", 0),
            "horizontal": genmtx(5, "h", 0),
        }
    },
    "6x6": {
        "1": {
            "upwards_diagonal": genmtx(6, "upd", 1),
            "downwards_diagonal": genmtx(6, "dwd", 1),
            "vertical": genmtx(6, "v", 1),
            "horizontal": genmtx(6, "h", 1),
        },
        "0": {
            "upwards_diagonal": genmtx(6, "upd", 0),
            "downwards_diagonal": genmtx(6, "dwd", 0),
            "vertical": genmtx(6,"v", 0),
            "horizontal": genmtx(6, "h", 0),
        }
    },
    "7x7": {
        "1": {
            "upwards_diagonal": genmtx(7, "upd", 1),
            "downwards_diagonal": genmtx(7, "dwd", 1),
            "vertical": genmtx(7, "v", 1),
            "horizontal": genmtx(7, "h", 1),
        },
        "0": {
            "upwards_diagonal": genmtx(7, "upd", 0),
            "downwards_diagonal": genmtx(7, "dwd", 0),
            "vertical": genmtx(7,"v", 0),
            "horizontal": genmtx(7, "h", 0),
        }
    },
    "8x8": {
        "1": {
            "upwards_diagonal": genmtx(8, "upd", 1),
            "downwards_diagonal": genmtx(8, "dwd", 1),
            "vertical": genmtx(8, "v", 1),
            "horizontal": genmtx(8, "h", 1),
        },
        "0": {
            "upwards_diagonal": genmtx(8, "upd", 0),
            "downwards_diagonal": genmtx(8, "dwd", 0),
            "vertical": genmtx(8, "v", 0),
            "horizontal": genmtx(8, "h", 0),
        }
    }  
}

def show_pretty(test_case: dict):
    results = []
    for size, cases in test_case.items():
        for active, methods in cases.items():
            print("\n=================================")
            print(f"{Col.blue}Size: {Col.gray}{size}, {Col.orange}Active: {Col.gray}{active}{Col.reset}")
            print("=================================")
            for method, matrix in methods.items():
                result = check_win(matrix)
                print("-----------------------------")
                print(f"{Col.green}Method: {Col.gray}{method}{Col.reset}, {Col.orange}Active: {Col.gray}{active}")
                print(f"{Col.red}Result: {Col.white}{result}{Col.reset}")

                if result == True:
                    results.append(True)
                    
    print("\n")
    
    if all(results):
        print(f"{Col.light_green}All test cases passed!{Col.reset}")
    else:
        print(f"{Col.light_red}Some test cases failed!{Col.reset}")
    
    print("\n")

if __name__ == "__main__":
    show_pretty(test_cases)