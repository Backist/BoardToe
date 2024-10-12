"""
Benchmark and test performance of win check algorithm.

Copyright Backist 2022-2024 under license GPL 3.0.
"""

from src.utils import gen_model_mtx
from src.termui.colors import Color

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

def print_matrix(matrix):
    for row in matrix:
        print(" | ".join(str(cell) for cell in row))
        print("_" * (len(row) * 4 - 1))  # Dibuja una línea entre las filas
        
test_cases = {
    "3x3": {
        "1": {
            "upwards_diagonal": gen_model_mtx(3, "upd", 1),
            "downwards_diagonal": gen_model_mtx(3, "dwd", 1),
            "vertical": gen_model_mtx(3, "v", 1),
            "horizontal": gen_model_mtx(3, "h", 1),
        },
        "0": {
            "upwards_diagonal": gen_model_mtx(3, "upd", 0),
            "downwards_diagonal": gen_model_mtx(3, "dwd", 0),
            "vertical": gen_model_mtx(3, "v", 0),
            "horizontal": gen_model_mtx(3, "h", 0),
        }
    },
    "4x4": {
        "1": {
            "upwards_diagonal": gen_model_mtx(4, "upd", 1),
            "downwards_diagonal": gen_model_mtx(4, "dwd", 1),
            "vertical": gen_model_mtx(4, "v", 1),
            "horizontal": gen_model_mtx(4, "h", 1),
        },
        "0": {
            "upwards_diagonal": gen_model_mtx(4, "upd", 0),
            "downwards_diagonal": gen_model_mtx(4, "dwd", 0),
            "vertical": gen_model_mtx(4, "v", 0),
            "horizontal": gen_model_mtx(4, "h", 0),
        }
    },
    "5x5": {
        "1": {
            "upwards_diagonal": gen_model_mtx(5, "upd", 1),
            "downwards_diagonal": gen_model_mtx(5, "dwd", 1),
            "vertical": gen_model_mtx(5, "v", 1),
            "horizontal": gen_model_mtx(5, "h", 1),
        },
        "0": {
            "upwards_diagonal": gen_model_mtx(5, "upd", 0),
            "downwards_diagonal": gen_model_mtx(5, "dwd", 0),
            "vertical": gen_model_mtx(5,"v", 0),
            "horizontal": gen_model_mtx(5, "h", 0),
        }
    },
    "6x6": {
        "1": {
            "upwards_diagonal": gen_model_mtx(6, "upd", 1),
            "downwards_diagonal": gen_model_mtx(6, "dwd", 1),
            "vertical": gen_model_mtx(6, "v", 1),
            "horizontal": gen_model_mtx(6, "h", 1),
        },
        "0": {
            "upwards_diagonal": gen_model_mtx(6, "upd", 0),
            "downwards_diagonal": gen_model_mtx(6, "dwd", 0),
            "vertical": gen_model_mtx(6,"v", 0),
            "horizontal": gen_model_mtx(6, "h", 0),
        }
    },
    "7x7": {
        "1": {
            "upwards_diagonal": gen_model_mtx(7, "upd", 1),
            "downwards_diagonal": gen_model_mtx(7, "dwd", 1),
            "vertical": gen_model_mtx(7, "v", 1),
            "horizontal": gen_model_mtx(7, "h", 1),
        },
        "0": {
            "upwards_diagonal": gen_model_mtx(7, "upd", 0),
            "downwards_diagonal": gen_model_mtx(7, "dwd", 0),
            "vertical": gen_model_mtx(7,"v", 0),
            "horizontal": gen_model_mtx(7, "h", 0),
        }
    },
    "8x8": {
        "1": {
            "upwards_diagonal": gen_model_mtx(8, "upd", 1),
            "downwards_diagonal": gen_model_mtx(8, "dwd", 1),
            "vertical": gen_model_mtx(8, "v", 1),
            "horizontal": gen_model_mtx(8, "h", 1),
        },
        "0": {
            "upwards_diagonal": gen_model_mtx(8, "upd", 0),
            "downwards_diagonal": gen_model_mtx(8, "dwd", 0),
            "vertical": gen_model_mtx(8, "v", 0),
            "horizontal": gen_model_mtx(8, "h", 0),
        }
    }  
}

def show_pretty(test_case: dict):
    results = []
    for size, cases in test_case.items():
        for active, methods in cases.items():
            print("\n=================================")
            print(f"{Color.BLUE}Size: {Color.LIGHT_GRAY}{size}, {Color.YELLOW}Active: {Color.LIGHT_GRAY}{active}{Color.RESET}")
            print("=================================")
            for method, matrix in methods.items():
                result = check_win(matrix)
                print("-----------------------------")
                print(f"{Color.GREEN}Method: {Color.LIGHT_GRAY}{method}{Color.RESET}, {Color.YELLOW}Active: {Color.LIGHT_GRAY}{active}")
                print(f"{Color.RED}Result: {Color.WHITE}{result}{Color.RESET}")

                if result is True:
                    results.append(True)
                    
    print("\n")
    
    if all(results):
        print(f"{Color.LIGHT_GREEN}All test cases passed!{Color.RESET}")
    else:
        print(f"{Color.LIGHT_RED}Some test cases failed!{Color.RESET}")
    
    print("\n")


if __name__ == "__main__":
    show_pretty(test_cases)