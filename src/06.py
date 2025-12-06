import re
import time

import numpy as np

EXAMPLE = """
123 328  51 64 
 45 64  387 23 
  6 98  215 314
*   +   *   +  
"""


def parse_input_part1(text: str) -> tuple[np.ndarray, np.ndarray]:
    lines = re.sub(r" +", " ", text).strip().split("\n")
    numbers = np.array([list(map(int, line.strip().split(" "))) for line in lines[:-1]])
    multiply = np.array(
        [True if operation == "*" else False for operation in lines[-1].strip().split(" ")]
    )
    assert numbers.shape[1] == len(multiply)
    addition_numbers = numbers[:, ~multiply]
    multiplication_numbers = numbers[:, multiply]

    return addition_numbers, multiplication_numbers


def parse_input_part2(text: str) -> tuple[np.ndarray, np.ndarray]:
    lines = text.strip().split("\n")
    number_lines = lines[:-1]

    # Append space at the end of each line to avoid edge case distinction when splitting
    # the blocks later
    number_lines = [line + " " for line in number_lines]
    assert len(set(len(line) for line in number_lines)) == 1
    num_chars = len(number_lines[0])
    num_rows = len(number_lines)
    number_blocks = []
    block_start_idx = 0
    for j in range(num_chars):
        if all(number_lines[i][j] == " " for i in range(num_rows)):
            number_blocks.append([number_lines[i][block_start_idx: j] for i in range(num_rows)])
            block_start_idx = j + 1

    multiply = [
        True if operation == "*" else False
        for operation in re.sub(r" +", " ", lines[-1].strip()).split(" ")
    ]
    assert len(multiply) == len(number_blocks)

    addition_blocks = []
    multiplication_blocks = []
    for i, block in enumerate(number_blocks):
        assert len(set(len(line) for line in block)) == 1
        num_chars = len(block[0])
        block_numbers = []
        for j in range(num_chars):
            block_numbers.append("".join(block[i][j] for i in range(num_rows)))
        if multiply[i]:
            multiplication_blocks.append(list(map(int, block_numbers)))
        else:
            addition_blocks.append(list(map(int, block_numbers)))

    # Bring output to the same format as in part 1
    addition_numbers = np.zeros(
        (
            len(max(addition_blocks, key=lambda x: len(x))),
            len(addition_blocks),
        ),
        dtype=int,
    )
    multiplication_numbers = np.ones(
        (
            len(max(multiplication_blocks, key=lambda x: len(x))),
            len(multiplication_blocks),
        ),
        dtype=int,
    )
    for i, j in enumerate(addition_blocks):
        addition_numbers[:len(j), i] = j
    for i, j in enumerate(multiplication_blocks):
        multiplication_numbers[:len(j), i] = j

    return addition_numbers, multiplication_numbers


def get_grand_totals(addition_numbers: np.ndarray, multiplication_numbers: np.ndarray) -> int:
    return addition_numbers.sum() + multiplication_numbers.prod(axis=0).sum()


if __name__ == "__main__":
    with open("../inputs/06.txt", "r") as fh:
        in_text = fh.read()

    # PART 1
    start = time.perf_counter()
    numbers_to_add, numbers_to_multiply = parse_input_part1(in_text)
    res = get_grand_totals(numbers_to_add, numbers_to_multiply)
    end = time.perf_counter()
    print(f"Part 1 Result: {res}. Took {(end - start) * 1000:.2f} ms.")

    # PART 2
    start = time.perf_counter()
    numbers_to_add, numbers_to_multiply = parse_input_part2(in_text)
    res = get_grand_totals(numbers_to_add, numbers_to_multiply)
    end = time.perf_counter()
    print(f"Part 2 Result: {res}. Took {(end - start) * 1000:.2f} ms.")
