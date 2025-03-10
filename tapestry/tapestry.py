from pycsp3 import *


def solve_tapestry(clues: list[list[(int, int)]]) -> list[list[(int, int)]]:
    
    n = len(clues)
    
    if (n==0) :
        return None
    if (len(clues[0]) != n) :
        return None
    
    x = VarArray(size=[n, n, 2], dom=(range(1, n+1)))
    y = VarArray(size=n*n, dom=range(1*n+1,n*(n+1)+1))

    satisfy(
        # natural constraints
        [y[i*n+j] == x[i][j][0]*n + x[i][j][1] for i in range(n) for j in range(n)],
        
        # constraint rows
        [AllDifferent(x[i, :, 0]) for i in range(n)],
        [AllDifferent(x[i, :, 1]) for i in range(n)],

        # constraint cols
        [AllDifferent(x[:, j, 0]) for j in range(n)],
        [AllDifferent(x[:, j, 1]) for j in range(n)],

        # constraint all different
        [AllDifferent(y)],

        # constraint clues
        [x[i][j][0] == clues[i][j][0] for i in range(n) for j in range(n) if clues and clues[i][j][0] > 0],
        [x[i][j][1] == clues[i][j][1] for i in range(n) for j in range(n) if clues and clues[i][j][1] > 0]
    )

    if solve(solver=CHOCO) is SAT:
        v = values(x)
        print(v)
        tab = []
        for i in range(n) :
            line = []
            for j in range(n) :
                line.append((v[i][j][0],v[i][j][1]))
            tab.append(line)
        return(tab)
    
    return None

def verify_format(solution: list[list[(int, int)]], n: int):
    validity = True
    if (len(solution) != n):
        validity = False
        print("The number of rows in the solution is not equal to n")
    for i in range(len(solution)):
        if len(solution[i]) != n:
            validity = False
            print(f"Row {i} does not contain the right number of cells\n")
        for j in range(len(solution[i])):
            if (not isinstance(solution[i][j], tuple)):
                validity = False
                print(f"Cell in row {i} and column {j} is not a tuple\n")
            elif len(solution[i][j]) != 2:
                validity = False
                print(f"Cell in row {i} and column {j} does not contain the right number of values\n")
    return validity

def parse_instance(input_file: str) -> list[list[(int, int)]]:
    with open(input_file) as input:
        lines = input.readlines()
    n = int(lines[0].strip())
    clues = [[(0, 0) for i in range(n)] for j in range(n)]
    for line in lines[1:]:
        i, j, s, c = line.strip().split(" ")
        clues[int(i)][int(j)] = (int(s), int(c))
    return n, clues

def print_solution(solution,n) :
    for i in range(n) :
        print (solution[i])

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 tapestry.py instance_path")
        sys.exit(1)

    n, clues = parse_instance(sys.argv[1])
    
    solution = solve_tapestry(clues)
    if solution is not None:
        if (verify_format(solution, n)):
            print("Solution format is valid")
            print_solution(solution,n)
        else:
            print("Solution format is invalid")
    else:
        print("No solution found")

