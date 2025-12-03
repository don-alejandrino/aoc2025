import functools
import time

import numpy as np


EXAMPLE = """
987654321111111
811111111111119
234234234234278
818181911112111
"""


def parse_input(text: str) -> list[str]:
    return [line.strip() for line in text.strip().split("\n")]


@functools.cache
def get_max_joltage(row_str_repr: str, sequence_length: int) -> int:
    row = np.array(list(map(int, list(row_str_repr))))
    row_length = len(row)
    max_digit = np.max(row)
    if sequence_length == 1:
        return max_digit
    for n in range(max_digit, 0, -1):
        highest_first_digit_positions = np.where(row == n)[0]
        relevant_highest_first_digit_positions = highest_first_digit_positions[np.where(
            highest_first_digit_positions < row_length - (
                sequence_length - 1))]
        if relevant_highest_first_digit_positions.shape[0] == 0:
            # Digit does not occur in the row OR all occurrences of the digit are so late in the row
            # that a sequence of length `sequence_length` can't be formed. Continue with the next
            # smaller number in this case.
            continue
        highest_tail_candidates: list[int] = []
        for position in relevant_highest_first_digit_positions:
            highest_tail_candidates.append(
                get_max_joltage(
                    row_str_repr[position + 1:], sequence_length - 1
                )
            )

        return n * 10 ** (sequence_length - 1) + max(highest_tail_candidates)

    raise ValueError(f"Sequence of length {sequence_length} could not be found.")


def sum_max_joltages(rows: list[str], sequence_length: int) -> int:
    max_joltages = []
    for row in rows:
        max_joltages.append(get_max_joltage(row, sequence_length))

    return sum(max_joltages)


if __name__ == "__main__":
    with open("../inputs/03.txt", "r") as fh:
        in_text = fh.read()

    battery_grid = parse_input(in_text)

    # PART 1
    start = time.perf_counter()
    res = sum_max_joltages(battery_grid, sequence_length=2)
    end = time.perf_counter()
    print(f"Part 1 Result: {res}. Took {(end - start) * 1000:.2f} ms.")

    # PART 2
    start = time.perf_counter()
    res = sum_max_joltages(battery_grid, sequence_length=12)
    end = time.perf_counter()
    print(f"Part 2 Result: {res}. Took {(end - start) * 1000:.2f} ms.")
