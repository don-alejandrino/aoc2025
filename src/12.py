import math
import time

import numpy as np

EXAMPLE = """
0:
###
##.
##.

1:
###
##.
.##

2:
.##
###
##.

3:
##.
###
##.

4:
###
#..
###

5:
###
.#.
###

4x4: 0 0 0 0 2 0
12x5: 1 0 1 0 2 2
12x5: 1 0 1 0 3 2
"""


def parse_input(
    text: str,
) -> tuple[list[np.ndarray], list[tuple[tuple[int, int], list[int]]]]:
    blocks = text.strip().split("\n\n")

    shapes = []
    for block in blocks[:-1]:
        rows = block.strip().splitlines()[1:]
        n_rows = len(rows)
        n_cols = len(rows[0])
        grid = np.zeros((n_rows, n_cols), dtype=bool)
        for i, row in enumerate(rows):
            for j, pos in enumerate(row):
                if pos == "#":
                    grid[i, j] = True
        shapes.append(grid)

    regions_str = blocks[-1].strip().splitlines()
    regions = []
    for region_str in regions_str:
        grid_size_str, required_shapes_str = region_str.split(":")
        grid_size = tuple(map(int, grid_size_str.split("x")))
        required_shapes = list(map(int, required_shapes_str.strip().split()))
        regions.append((grid_size, required_shapes))

    return shapes, regions


def is_packaging_possible_because_of_area(
    shapes: list[np.ndarray],
    region: tuple[tuple[int, int], list[int]],
) -> bool:
    max_area = math.prod(region[0])
    required_area = sum(num * shapes[i].sum() for i, num in enumerate(region[1]))

    return max_area >= required_area


def get_number_of_packaging_possible(
    shapes: list[np.ndarray],
    regions: list[tuple[tuple[int, int], list[int]]],
) -> int:
    """
    Obviously, only checking whether the sum of the area of all required shapes fits
    into a region is not sufficient to determine whether the shapes can actually be
    packed into the region without overlap. However, it is a necessary condition, so
    we can use it to prune the problem and rule out some combinations right from the
    beginning.
    It turns out, however, thet the problem input was designed so that this simple check
    is enough to solve the problem (otherwise, designing an optimal packaging solver for
    a problem of this size would be a really heavy challenge).
    Note also (it's a bit mean) that with the example input, this simple strategy does
    not work, but only with the actual problem input.

    """
    return sum(
        is_packaging_possible_because_of_area(shapes, region) for region in regions
    )


if __name__ == "__main__":
    with open("../inputs/12.txt", "r") as fh:
        in_text = fh.read()

    gift_shapes, gift_regions = parse_input(in_text)

    start = time.perf_counter()
    res = get_number_of_packaging_possible(gift_shapes, gift_regions)
    end = time.perf_counter()
    print(f"Part 1 Result: {res}. Took {(end - start) * 1000:.2f} ms.")
