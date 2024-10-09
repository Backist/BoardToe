import pyperf
from typing import Dict, Tuple, Any



# Definición de la tabla inicial
table = [
    ["0", "0", "-"],
    ["X", "-", "X"],
    ["-", "0", "0"]
]


# /////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
def empty_list_method_1() -> list:
    return [['-' for _ in range(len(table))] for _ in range(len(table))]

def empty_list_method_2() -> list:
    master_table = []
    for _ in range(len(table)):
        master_table.append(['-' for _ in range(len(table))])
    return master_table

def replace_by_index_1() -> None:
    for i in range(len(table)):
        for j in range(len(table)):
            if table[i][j] == "-":
                table[i][j] = -1
            elif table[i][j] == "0":
                table[i][j] = 0
            elif table[i][j] == "X":
                table[i][j] = 1

def replace_by_index_2() -> list:
    t = []
    for i in range(len(table)):
        row = []
        for j in range(len(table)):
            if table[i][j] == "-":
                row.append(-1)
            elif table[i][j] == "0":
                row.append(0)
            elif table[i][j] == "X":
                row.append(1)
        t.append(row)
    return t

# Ejemplo de funciones adicionales para los tests del bot
def check_matrix_1(matrix: list[int]) -> bool | list[tuple[int, tuple[int, int]]]:
    results = []
    for i, subarray in enumerate(matrix):
        if all(elem == -1 for elem in subarray) or all(elem == subarray[0] for elem in subarray):
            continue
        elif subarray.count(-1) == 1:
            empty_index = subarray.index(-1)
            if all(x == subarray[i] for x in subarray if subarray.index(x) != empty_index):
                results.append((subarray[i], (i, empty_index)))
    return results

def check_matrix_2(matrix: list[int]) -> bool | list[tuple[int, tuple[int, int]]]:
    results = []
    for i, subarray in enumerate(matrix):
        if all(elem == -1 for elem in subarray) or all(elem == subarray[0] for elem in subarray):
            continue
        elif subarray.count(-1) == 1:
            empty_index = subarray.index(-1)
            if len(set(subarray)) == 2:
                results.append((subarray[i], (i, empty_index)))
    return results

def rotate_index_tuple2list(index: list[tuple[int, int]], depth: int) -> list[tuple[int, int]]:
    if not index:
        return None
    index = [list(i) for i in index]
    for i in index:
        temp = i[1]
        i[1] = i[0]
        i[0] = depth - 1 - temp
    return [tuple(i) for i in index]

def rotate_index_without_conversion(index: list[list[int, int]], depth: int) -> list[tuple[int, int]]:
    if not index:
        return None
    for i in index:
        temp = i[1]
        i[1] = i[0]
        i[0] = depth - 1 - temp
    return index


# /////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

def run_benchmark() -> None:
    """
    Executes a series of performance benchmarks using the pyperf library.

    This function sets up a benchmarking runner and defines various test functions to measure their performance. 
    It includes benchmarks for methods that operate on empty lists and those that manipulate matrices, 
    allowing for performance comparisons across different implementations.
    """

    runner = pyperf.Runner()

    # Definir los tests
    runner.bench_func('Empty list method 1', empty_list_method_1)
    runner.bench_func('Empty list method 2', empty_list_method_2)
    runner.bench_func('Replace by index 1', replace_by_index_1)
    runner.bench_func('Replace by index 2', replace_by_index_2)

    # Agregar más pruebas
    runner.bench_func('Check matrix 1', check_matrix_1, table)
    runner.bench_func('Check matrix 2', check_matrix_2, table)


if __name__ == "__main__":
    run_benchmark()
