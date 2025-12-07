import time

import numpy as np

EXAMPLE = """
.......S.......
...............
.......^.......
...............
......^.^......
...............
.....^.^.^.....
...............
....^.^...^....
...............
...^.^...^.^...
...............
..^...^.....^..
...............
.^.^.^.^.^...^.
...............
"""


CHAR_TO_INT_MAPPING = {
    ".": 0,
    "S": 1,
    "^": -1,
}


def parse_input(text: str) -> np.ndarray:
    lines = text.strip().split("\n")
    return np.array(
        [
            list(map(lambda char: CHAR_TO_INT_MAPPING[char], list(line.strip())))
            for line in lines
        ],
        dtype=int
    )


def simulate_beam(grid: np.ndarray) -> np.ndarray:
    # Whenever a beam crosses an empty space cell, its value is increased by one. Whenever a beam
    # hits a splitter, the value of the splitter is decreased by one. Together with the starting
    # conditions (empty cells start with 0, splitters start with -1), this way we can easily count
    # the number of paths (i.e., how often an empty cell space was crossed and how often a splitter
    # was hit) while always being able to decide between splitter and empty space cells.
    grid = grid.copy()
    for i in range(grid.shape[0] - 1):
        for j in range(grid.shape[1]):
            if grid[i, j] > 0:
                # At least one beam path goes through cell
                if grid[i + 1, j] >= 0:
                    # Propagate the beams through next downstream cell
                    grid[i + 1, j] += grid[i, j]
                elif grid[i + 1, j] < 0:
                    # Next downstream cell is a splitter
                    grid[i + 1, j] -= grid[i, j]
            elif grid[i, j] < -1:
                # Activated splitter (i.e., splitter hit by at least one beam path)
                # -> split the beam into two
                for k in (j - 1, j + 1):
                    if grid[i + 1, k] >= 0:
                        grid[i + 1, k] += -grid[i, j] - 1
                    elif grid[i + 1, k] < 0:
                        grid[i + 1, k] -= -grid[i, j] - 1

    return grid


def count_num_activated_splitters(grid: np.ndarray) -> int:
    return (grid < -1).sum()


def count_num_paths(grid: np.ndarray) -> int:
    return grid[-1, :].sum()


if __name__ == "__main__":
    with open("../inputs/07.txt", "r") as fh:
        in_text = fh.read()

    # PART 1
    start = time.perf_counter()
    beam_grid = simulate_beam(parse_input(in_text))
    res = count_num_activated_splitters(beam_grid)
    end = time.perf_counter()
    print(f"Part 1 Result: {res}. Took {(end - start) * 1000:.2f} ms.")

    # PART 2
    start = time.perf_counter()
    res = count_num_paths(beam_grid)
    end = time.perf_counter()
    print(f"Part 2 Result: {res}. Took {(end - start) * 1000:.2f} ms.")
