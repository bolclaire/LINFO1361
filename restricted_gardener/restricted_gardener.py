from pycsp3 import *


def solve_restricted_gardener(instruction: int, n:int) -> list[int]:
    # Put your code here
    X = VarArray(size = n, dom=range(1,n+1))
    sub_x = VarArray(size = n-1, dom=range(0,2))

    satisfy(
        AllDifferent(X),
        [sub_x[i-1] == (Maximum(X[:i]) < X[i]) for i in range(1,n)],
        Sum(sub_x) == instruction-1
    )

    if solve(solver= CHOCO) is SAT:
        return values(X)

    return None

def verify_format(solution: list[int], n: int):
    if len(solution) != n:
        print(f"The solution does not contain the right number of cells\n")
        for i in range(len(solution)):
            if (not isinstance(solution[i], int)):
                print(f"Cell at index {i} is not an integer\n")

def parse_instance(input_file: str) -> tuple[int, int]:
    with open(input_file, "r") as file:
        lines = file.readlines()
    n = int(lines[0].strip())
    instruction = int(lines[1].strip())

    return instruction, n


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 restricted_gardener.py instance_path")
        sys.exit(1)

    instruction, n  = parse_instance(sys.argv[1])


    solution = solve_restricted_gardener(instruction, n)
    if solution is not None:
        if (verify_format(solution, n)):
            print("Solution format is valid")
        else:
            print("Solution is invalid")
    else:
        print("No solution found")
