import time

import numpy as np

EXAMPLE = """
7,1
11,1
11,7
9,7
9,5
2,5
2,3
7,3
"""


def parse_input(text: str) -> list[np.ndarray]:
    return [np.array(list(map(int, line.strip().split(",")))) for line in text.strip().split("\n")]


def build_area_map(points: list[np.ndarray]) -> np.ndarray:
    area_map = np.zeros((len(points), len(points)), dtype=int)
    for i, p1 in enumerate(points):
        for j, p2 in enumerate(points):
            if j >= i:
                continue
            area_map[i, j] = (np.abs(p1 - p2) + np.array([1, 1])).prod()

    return area_map


def compress_points(
    points: list[np.ndarray]
) -> tuple[list[np.ndarray], dict[int, int], dict[int, int]]:
    # Don't start with zero, so that compressed points never touch the border of their grid.
    # This way, we can easily floodfill the grid from the outside.
    orig_to_compressed_x_coords_mapping = {
        x: i + 1 for i, x in enumerate(sorted(set([p[0] for p in points])))
    }
    orig_to_compressed_y_coords_mapping = {
        y: i + 1 for i, y in enumerate(sorted(set([p[1] for p in points])))
    }
    compressed_points = [
        np.array(
            [orig_to_compressed_x_coords_mapping[p[0]], orig_to_compressed_y_coords_mapping[p[1]]]
        )
        for p in points
    ]
    compressed_to_orig_x_coords_mapping = {
        v: k for k, v in orig_to_compressed_x_coords_mapping.items()
    }
    compressed_to_orig_y_coords_mapping = {
        v: k for k, v in orig_to_compressed_y_coords_mapping.items()
    }
    return (
        compressed_points,
        compressed_to_orig_x_coords_mapping,
        compressed_to_orig_y_coords_mapping,
    )


def floodfill(grid: np.ndarray) -> np.ndarray:
    grid = grid.copy()
    coords_to_visit = [[0, 0]]
    i_max, j_max = grid.shape
    while coords_to_visit:
        i, j = coords_to_visit.pop()
        if grid[i, j] == 1:
            grid[i, j] = 0
            if j + 1 < j_max:
                coords_to_visit.append([i, j + 1])
            if j - 1 >= 0:
                coords_to_visit.append([i, j - 1])
            if i + 1 < i_max:
                coords_to_visit.append([i + 1, j])
            if i - 1 >= 0:
                coords_to_visit.append([i - 1, j])

    return grid


def fill_contour(grid_points: list[np.ndarray]) -> np.ndarray:
    """
    Strategy:
    1. Start on a grid filled with ones.
    2. Set every cell on the contour itself to two.
    3. Finally, floodfill the grid with zeros, starting "outside" of the contour.

    """
    i_max = max(grid_points, key=lambda p: p[0])[0]
    j_max = max(grid_points, key=lambda p: p[1])[1]
    arr = np.ones((i_max + 1, j_max + 2), dtype=np.int8)
    for n, point in enumerate(grid_points):
        next_point = grid_points[n + 1] if n < len(grid_points) - 1 else grid_points[0]
        if next_point[0] > point[0]:
            arr[point[0]:next_point[0], point[1]] = 2
        elif next_point[0] < point[0]:
            arr[next_point[0]:point[0], point[1]] = 2
        elif next_point[1] > point[1]:
            arr[point[0], point[1]:next_point[1]] = 2
        elif next_point[1] < point[1]:
            arr[point[0], next_point[1]:point[1]] = 2
        else:
            raise ValueError("Points are not unique.")

    return floodfill(arr)


def find_area_of_largest_filled_rectangle(
    compressed_points: list[np.ndarray],
    compressed_to_orig_x_coords_mapping: dict[int, int],
    compressed_to_orig_y_coords_mapping: dict[int, int],
) -> int:
    """
    The approach to find the largest rectangle that is filled (i.e., consists of red or green tiles
    only) is basically brute-force, i.e., for every possible rectangle, we check whether it has
    only red or green tiles in it. What makes this approach feasible is the initial compression
    of the red tile coordinates by considering their sorted index instead of their actual values.
    That is, the lowest x coordinate is assigned to 1, the second-lowest one to 2, and so on
    (likewise for the y coordinates). This way, distances between the points are compressed
    in a variable way, while still preserving the order of the points in both their coordinates.
    Accordingly, we can also tell from the compressed coordinates whether a rectangle consists of
    red or green tiles only. For the calculation of the rectangles' areas, however, we have to
    transform the compressed coordinates back to the original ones.

    """
    # Red or green tiles are where filled_grid is equal to 2 (contour defined by the red tiles)
    # or 1 (interior of the contour)
    filled_grid = fill_contour(compressed_points)
    max_area = 0
    for i, p1 in enumerate(compressed_points):
        for j, p2 in enumerate(compressed_points):
            if j >= i:
                continue
            if p2[0] >= p1[0]:
                x_lower = p1[0]
                x_upper = p2[0]
            else:
                x_lower = p2[0]
                x_upper = p1[0]
            if p2[1] >= p1[1]:
                y_lower = p1[1]
                y_upper = p2[1]
            else:
                y_lower = p2[1]
                y_upper = p1[1]
            if (filled_grid[x_lower:x_upper + 1, y_lower:y_upper + 1] == 0).any():
                continue
            area = (
                (
                    compressed_to_orig_x_coords_mapping[x_upper] -
                    compressed_to_orig_x_coords_mapping[x_lower]
                    + 1
                ) *
                (
                    compressed_to_orig_y_coords_mapping[y_upper] -
                    compressed_to_orig_y_coords_mapping[y_lower]
                    + 1
                )
            )
            if area > max_area:
                max_area = area

    return max_area


if __name__ == "__main__":
    with open("../inputs/09.txt", "r") as fh:
        in_text = fh.read()

    red_tiles = parse_input(in_text)

    # PART 1
    start = time.perf_counter()
    res = build_area_map(red_tiles).max()
    end = time.perf_counter()
    print(f"Part 1 Result: {res}. Took {(end - start) * 1000:.2f} ms.")

    # PART 2
    start = time.perf_counter()
    res = find_area_of_largest_filled_rectangle(*compress_points(red_tiles))
    end = time.perf_counter()
    print(f"Part 2 Result: {res}. Took {(end - start) * 1000:.2f} ms.")
