import time

import numpy as np


EXAMPLE = """
..@@.@@@@.
@@@.@.@.@@
@@@@@.@.@@
@.@@@@..@.
@@.@@@@.@@
.@@@@@@@.@
.@.@.@.@@@
@.@@@.@@@@
.@@@@@@@@.
@.@.@@@.@.
"""


def parse_input(text: str) -> np.ndarray:
    rows = text.strip().split("\n")
    n_rows = len(rows)
    n_cols = len(rows[0])
    # Pad array with zeros (walls count like "no neighbor") to avoid dedicated
    # handling of the array boundaries in `get_num_accessible_paper_rolls_in_one_step`
    grid = np.zeros((n_rows + 2, n_cols + 2), dtype=int)
    for i, row in enumerate(rows):
        for j, pos in enumerate(row):
            if pos == "@":
                grid[i + 1, j + 1] = True

    return grid


def get_num_accessible_paper_rolls_in_one_step(grid: np.ndarray) -> tuple[int, np.ndarray]:
    new_grid = grid.copy()
    num_accessible_paper_rolls = 0
    n_rows, n_cols = grid.shape
    for i in range(1, n_rows - 1):
        for j in range(1, n_cols - 1):
            if not grid[i, j]:
                continue
            num_neighbors = (
                grid[i - 1, j - 1] + grid[i - 1, j] + grid[i - 1, j + 1] +
                grid[i, j - 1] + grid[i, j + 1] +
                grid[i + 1, j - 1] + grid[i + 1, j] + grid[i + 1, j + 1]
            )
            if num_neighbors < 4:
                num_accessible_paper_rolls += 1
                new_grid[i, j] = 0

    return num_accessible_paper_rolls, new_grid


def get_overall_num_accessible_paper_rolls(grid: np.ndarray) -> int:
    overall_num_accessible_paper_rolls = 0
    num_accessible_paper_rolls = -1
    while num_accessible_paper_rolls != 0:
        num_accessible_paper_rolls, new_grid = get_num_accessible_paper_rolls_in_one_step(grid)
        overall_num_accessible_paper_rolls += num_accessible_paper_rolls
        grid = new_grid

    return overall_num_accessible_paper_rolls


if __name__ == "__main__":
    with open("../inputs/04.txt", "r") as fh:
        in_text = fh.read()

    paper_roll_grid = parse_input(in_text)

    # PART 1
    start = time.perf_counter()
    res, _ = get_num_accessible_paper_rolls_in_one_step(paper_roll_grid)
    end = time.perf_counter()
    print(f"Part 1 Result: {res}. Took {(end - start) * 1000:.2f} ms.")

    # PART 2
    start = time.perf_counter()
    res = get_overall_num_accessible_paper_rolls(paper_roll_grid)
    end = time.perf_counter()
    print(f"Part 2 Result: {res}. Took {(end - start) * 1000:.2f} ms.")
