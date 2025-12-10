import re
import time
from itertools import product
from typing import Literal, Callable

import cvxpy as cp
import numpy as np

EXAMPLE = """
[.##.] (3) (1,3) (2) (2,3) (0,2) (0,1) {3,5,4,7}
[...#.] (0,2,3,4) (2,3) (0,4) (0,1,2) (1,2,3,4) {7,5,12,7,2}
[.###.#] (0,1,2,3,4) (0,3,4) (0,1,2,4,5) (1,2) {10,11,11,5,10,5}
"""


def parse_input(text: str, part: Literal[1, 2]) -> list[tuple[np.ndarray, np.ndarray]]:
    equations = []
    for line in text.strip().splitlines():
        if part == 1:
            rhs_match = re.match(r"\[([.#]+)]", line)
            if rhs_match is None:
                raise ValueError(f"Invalid input: {line}")
            rhs_str = rhs_match.group(1).replace(".", "0").replace("#", "1")
            rhs = np.array(list(map(int, list(rhs_str))))
        elif part == 2:
            rhs_match = re.search(r"\{([\d,]+)}", line)
            if rhs_match is None:
                raise ValueError(f"Invalid input: {line}")
            rhs_str = rhs_match.group(1)
            rhs = np.array(list(map(int, rhs_str.strip().split(","))))
        else:
            raise ValueError(f"Invalid part: {part}")

        lhs_match = re.search(r"\([\d\s,()]+\)", line)
        if lhs_match is None:
            raise ValueError(f"Invalid input: {line}")
        lhs_str = lhs_match.group(0)
        lhs_coeffs = [
            (eval(tup),) if len(tup) == 3 else eval(tup)
            for tup in lhs_str.strip().split(" ")
        ]
        lhs = np.zeros((len(rhs), len(lhs_coeffs)), dtype=int)
        for i, coeff in enumerate(lhs_coeffs):
            lhs[coeff, i] = 1
        equations.append((lhs, rhs))

    return equations


def solve_minimization_problem_part1(
    equation: tuple[np.ndarray, np.ndarray],
) -> np.ndarray:
    """
    The minimization problem is linear and binary. Due to the sizes of the equation
    systems, we can solve it by simply trying all possible solutions (ordered by
    ascending cost) and stopping once we find a valid solution to the system of
    equations. This solution is then also the minimal solution.

    """
    lhs, rhs = equation
    # Pressing a button two times just undoes the first press -> Pressing any button
    # more than once doesn't make sense and can't lead to an optimal solution
    solution_candidates = list(map(np.array, product((0, 1), repeat=lhs.shape[1])))
    solution_candidates.sort(key=lambda x: x.sum())
    for solution_candidate in solution_candidates:
        if (np.mod(lhs.dot(solution_candidate), 2) == rhs).all():
            return solution_candidate
    raise ValueError("No solution found.")


def solve_minimization_problem_part2(
    equation: tuple[np.ndarray, np.ndarray],
) -> np.ndarray:
    """
    The equations are a system of linear Diophantine equations. A convenient way to
    minimize this problem is to apply an integer programming library.
    We need to minimize our target vector x (number of button presses for each button)
    under the constraints that lhs * x == rhs and x >= 0 and integer. Here, "*" is the
    matrix multiplication operator.

    """
    lhs, rhs = equation
    x_dim = lhs.shape[1]
    x = cp.Variable(x_dim, integer=True)

    # Define the constraints
    constraints = [x >= 0, lhs @ x - rhs == 0]

    # Define the minimization problem and solve it
    obj = cp.Minimize(cp.sum(x))
    prob = cp.Problem(obj, constraints)
    _sol = prob.solve(solver="ECOS_BB")

    return x.value.round(0).astype(int)


def sum_lowest_number_of_button_presses_for_all_machines(
    equations: list[tuple[np.ndarray, np.ndarray]],
    solver_fct: Callable[[tuple[np.ndarray, np.ndarray]], np.ndarray],
) -> int:
    out = 0
    for equation in equations:
        out += solver_fct(equation).sum()

    return out


if __name__ == "__main__":
    with open("../inputs/10.txt", "r") as fh:
        in_text = fh.read()

    # PART 1
    start = time.perf_counter()
    equations_list = parse_input(in_text, part=1)
    res = sum_lowest_number_of_button_presses_for_all_machines(
        equations_list, solve_minimization_problem_part1
    )
    end = time.perf_counter()
    print(f"Part 1 Result: {res}. Took {(end - start) * 1000:.2f} ms.")

    # PART 2
    start = time.perf_counter()
    equations_list = parse_input(in_text, part=2)
    res = sum_lowest_number_of_button_presses_for_all_machines(
        equations_list, solve_minimization_problem_part2
    )
    end = time.perf_counter()
    print(f"Part 2 Result: {res}. Took {(end - start) * 1000:.2f} ms.")
