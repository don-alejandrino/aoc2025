import time
from functools import cache

from frozendict import frozendict

EXAMPLE1 = """
aaa: you hhh
you: bbb ccc
bbb: ddd eee
ccc: ddd eee fff
ddd: ggg
eee: out
fff: out
ggg: out
hhh: ccc fff iii
iii: out
"""

EXAMPLE2 = """
svr: aaa bbb
aaa: fft
fft: ccc
bbb: tty
tty: ccc
ccc: ddd eee
ddd: hub
hub: fff
eee: dac
dac: fff
fff: ggg hhh
ggg: out
hhh: out
"""


def parse_input(text: str) -> dict[str, tuple[str]]:
    circuit_dict = {}
    lines = text.strip().splitlines()
    for line in lines:
        left, right = line.split(": ")
        circuit_dict[left.strip()] = tuple(right.strip().split(" "))

    return circuit_dict


@cache
def get_num_paths_to_terminal_nodes(
    circuit_dict: frozendict[str, tuple[str]],
    start_node: str = "you",
    end_node: str = "out",
    target_nodes: tuple[str, ...] = (),
    target_nodes_reached: tuple[str, ...] = (),
) -> int:
    if start_node == end_node:
        return 1 if set(target_nodes_reached) == set(target_nodes) else 0
    if start_node in target_nodes:
        target_nodes_reached += (start_node,)
    out = 0
    for next_node in circuit_dict[start_node]:
        out += get_num_paths_to_terminal_nodes(
            circuit_dict,
            next_node,
            end_node,
            target_nodes,
            target_nodes_reached,
        )

    return out


if __name__ == "__main__":
    with open("../inputs/11.txt", "r") as fh:
        in_text = fh.read()

    circuit = parse_input(in_text)

    # PART 1
    start = time.perf_counter()
    res = get_num_paths_to_terminal_nodes(frozendict(circuit), "you", "out")
    end = time.perf_counter()
    print(f"Part 1 Result: {res}. Took {(end - start) * 1000:.2f} ms.")

    # PART 2
    start = time.perf_counter()
    res = get_num_paths_to_terminal_nodes(
        frozendict(circuit),
        "svr",
        "out",
        target_nodes=("fft", "dac"),
    )
    end = time.perf_counter()
    print(f"Part 2 Result: {res}. Took {(end - start) * 1000:.2f} ms.")
