"Main file to benchmark the game performance and game algorithms"

from timeit import Timer

table = [
        ["0", "0", "-"],
        ["X", "-", "X"],
        ["-", "0", "0"]
    ]

def benchmark(stmt, n=1000, r=3, **kwargs):
    timer = Timer(stmt, **kwargs)
    best = min(timer.repeat(r, n))

    return best * 1e6 / n

def run_tests(title, dictests: dict):
    print(title)
    print("-"*60)
    for name, usec in dictests.items():
        print(f'\t{name:<12} | Time -> {usec:01.4f} μs\n')
    print("\tConvertion: 1 μs = 0.001 ms = 0.00001 s")
    print("-"*60)
    


tests1 = {
    
    "Empty list method 1": benchmark("[['-' for _ in range(len(table))] for _ in range(len(table))]", globals= {"table": table}),
    "Empty list method 2": benchmark(
    """
for _ in range(0, len(table)):
    master_table.append([])
for c in master_table:
        c.append("-" for _ in range(0, len(table)))
    """, globals= {"master_table": [], "table": table}
    ),
    "Replace by index 1": benchmark(
    """
for i in range(len(table)):
    for _ in range(len(table)):
        if table[i][_] == "-":
            table[i][_] = -1
        elif table[i][_] == "0":
            table[i][_] = 0
        elif table[i][_] == "X":
            table[i][_] = 1
    """ ,
        globals= {"table": table}
    ),
    "Replace by index 2": benchmark(
        """
t = []
for i in range(len(table)):
    for _ in range(len(table)):
        if table[i][_] == "-":
            t[i][_] = -1
        elif table[i][_] == "0":
            t[i][_] = 0
        elif table[i][_] == "X":
            t[i][_] = 1
        """ ,
        globals= {"table": table}
    )
}

bot_tests_suite = {
    "HCheck 1": benchmark(

        """
def check_matrix(matrix: list[int]) -> bool | list[tuple[int, tuple[int, int]]]:
    results: list[tuple[int, tuple[int, int]]] = []

    for i, subarray in enumerate(matrix):
        
        if all(elem == -1 for elem in subarray) or all(elem == subarray[0] for elem in subarray):
            continue
        elif subarray.count(-1) == 1:   
            empty_index: int = subarray.index(-1)
            if all(x == subarray[i] for x in subarray if subarray.index(x) != empty_index):
                results.append((subarray[i], (i, empty_index))) #* (jugador que gana, (posicion donde puede ganar))
    return results
        """, 
        n=20
    ),
    "HCheck 2": benchmark(

        """
def check_matrix(matrix: list[int]) -> bool | list[tuple[int, tuple[int, int]]]:
    results: list[tuple[int, tuple[int, int]]] = []

    for i, subarray in enumerate(matrix):

        if all(elem == -1 for elem in subarray) or all(elem == subarray[0] for elem in subarray):
            #* si alguna lista es totalmente vacia,  o son iguales, que continue 
            continue
        elif subarray.count(-1) == 1:   
            empty_index: int = subarray.index(-1)    # sabemos que las listas tienen al menos un -1, buscamos su indice
            if len(set(subarray)) == 2:
                results.append((subarray[i], (i, empty_index))) #* (jugador que gana, [posicion donde puede ganar])
    return results
        """, 
        n=2000
    ),

    "Rotate index tuple2list convertion": benchmark(

        """
def rotate_index(index: list[tuple[int, int]], depth: int) -> list[tuple[int, int]]:
    assert isinstance(index, list) or not index, "@index param must be list with indexs"

    if len(index) < 1:
        return None
    
    index = [list(i) for i in index]
    for i in index:
        temp = i[1]
        i[1] = i[0]
        i[0] = depth-1-temp
        index[index.index(i)] = i
    return [tuple(i) for i in index]
        """,
        n= 20
    ),

    "Rotate index without convertion": benchmark(

        """
def rotate_index(index: list[list[int, int]], depth: int) -> list[tuple[int, int]]:
    assert isinstance(index, list) or not index, "@index param must be list with indexs"

    if len(index) < 1:
        return None
    
    for i in index:
        temp = i[1]
        i[1] = i[0]
        i[0] = depth-1-temp
        index[index.index(i)] = i
    return index
        """,
        n= 20
    ),
}
        
run_tests("Pruebas 1", tests1)
run_tests("Bot Suite (Core)", bot_tests_suite)