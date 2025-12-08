import math
import time

import numpy as np

EXAMPLE = """
162,817,812
57,618,57
906,360,560
592,479,940
352,342,300
466,668,158
542,29,236
431,825,988
739,650,466
52,470,668
216,146,977
819,987,18
117,168,530
805,96,715
346,949,466
970,615,88
941,993,340
862,61,35
984,92,344
425,690,689
"""


def parse_input(text: str) -> list[np.ndarray]:
    return [np.array(list(map(int, line.strip().split(",")))) for line in text.strip().split("\n")]


def build_distance_map(points: list[np.ndarray]) -> np.ndarray:
    distance_map = np.ones((len(points), len(points)), dtype=float) * np.inf
    for i, p1 in enumerate(points):
        for j, p2 in enumerate(points):
            if j >= i:
                continue
            else:
                distance_map[i, j] = np.linalg.norm(p1 - p2)

    return distance_map


def connect_junctions(
    distance_map: np.ndarray,
    num_connections: int | None = None,
) -> tuple[list[set], tuple[int, int] | None]:
    """
    Return a tuple, where the first element are the connected clusters after connecting the
    `num_connections` nearest nodes (if `num_connections` is None, we're iterating over all possible
    connections, still sorted by distance). The second element are the indices of the last two
    nodes, the connection of which causes just one single cluster to remain that contains all the
    nodes.
    If `num_connections` is small enough, the function can return before all clusters were
    connected. In that case, the second element of the returned tuple is None.
    On the other hand, if we iterated long enough to find the last cluster-connecting edge,
    the first element of the returned tuple is a list with just one item, which is the set of all
    nodes.

    """
    idx_pairs_sorted = np.stack(
        np.unravel_index(distance_map.ravel().argsort(), distance_map.shape)
    ).T
    n_pairs = distance_map.shape[0] * (distance_map.shape[0] - 1) // 2
    if num_connections is None:
        idx_pairs_sorted = idx_pairs_sorted[:n_pairs]
    else:
        if num_connections > n_pairs:
            raise ValueError(
                f"`num_connections` is too large. Maximum possible value is {n_pairs}."
            )
        idx_pairs_sorted = idx_pairs_sorted[:num_connections]
    clusters = []
    for idx1, idx2 in idx_pairs_sorted:
        hit = -1
        for i, cluster in enumerate(clusters):
            if idx1 in cluster or idx2 in cluster:
                if hit == -1:
                    cluster.update((idx1, idx2))
                    hit = i
                elif hit != i:
                    # Other point of the idx tuple is already in another cluster
                    # -> Connect these two clusters
                    cluster.update((idx1, idx2))
                    cluster.update(clusters[hit])
                    del clusters[hit]
            if len(clusters) == 1 and clusters[0] == set(range(distance_map.shape[0])):
                # There is only one cluster left that contains all nodes. We abort here, since
                # adding additional connections can't change the cluster anymore.
                return clusters, (idx1, idx2)
        if hit == -1:
            clusters.append({idx1, idx2})

    return clusters, None


def multiply_size_of_n_largest_clusters(clusters: list[set], n: int = 3) -> int:
    return math.prod(sorted(map(len, clusters), reverse=True)[:n])


def multiply_x_coords_of_last_cluster_connecting_edge(
        node_idcs: tuple[int, int],
        node_positions: list[np.ndarray]
) -> int:
    return node_positions[node_idcs[0]][0] * node_positions[node_idcs[1]][0]


if __name__ == "__main__":
    with open("../inputs/08.txt", "r") as fh:
        in_text = fh.read()

    junction_box_positions = parse_input(in_text)

    # PART 1
    start = time.perf_counter()
    junction_box_distance_map = build_distance_map(junction_box_positions)
    res = multiply_size_of_n_largest_clusters(
        connect_junctions(junction_box_distance_map, 1000)[0]
    )
    end = time.perf_counter()
    print(f"Part 1 Result: {res}. Took {(end - start) * 1000:.2f} ms.")

    # PART 2
    start = time.perf_counter()
    res = multiply_x_coords_of_last_cluster_connecting_edge(
        connect_junctions(junction_box_distance_map, None)[1], junction_box_positions
    )
    end = time.perf_counter()
    print(f"Part 2 Result: {res}. Took {(end - start) * 1000:.2f} ms.")
