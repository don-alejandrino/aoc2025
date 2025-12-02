import time
from typing import Callable, Counter

EXAMPLE = """
11-22,95-115,998-1012,1188511880-1188511890,222220-222224,
1698522-1698528,446443-446449,38593856-38593862,565653-565659,
824824821-824824827,2121212118-2121212124
"""


def parse_input(text: str) -> list[tuple[int, int]]:
    id_ranges_str = text.strip().replace("\n", "").split(",")

    id_ranges = []
    for id_range_str in id_ranges_str:
        low, high = id_range_str.split("-")
        id_ranges.append((int(low), int(high)))

    return id_ranges


def get_invalid_ids_part1(id_range: tuple[int, int]) -> list[int]:
    out = []
    for i in range(id_range[0], id_range[1] + 1):
        i_str = str(i)
        i_digits = len(i_str)
        first_half = i_str[:i_digits // 2]
        second_half = i_str[i_digits // 2:]
        if first_half == second_half:
            out.append(i)

    return out


def get_invalid_ids_part2(id_range: tuple[int, int]) -> list[int]:
    out = []
    for i in range(id_range[0], id_range[1] + 1):
        i_str = str(i)
        i_digits = len(i_str)
        digits_counter = dict(Counter(i_str))

        # If the number `i` contains a repeated sequence,
        # i) every digit must occur at least twice
        if all(val > 1 for val in digits_counter.values()):
            min_freq = min(digits_counter.values())
            # ii) the occurrence of every digit must be an integer multiple of the occurrence of
            #     the least-frequent digit
            if all(val % min_freq == 0 for val in digits_counter.values()):
                sequence_length = i_digits // min_freq
                # iii) the overall number of digits must be an integer multiple of the sequence
                #      length, which is determined by the occurrence of the least-frequent digit
                if i_digits % sequence_length == 0:
                    # If the three preconditions above are met, we know that any repeated sequence
                    # (if it is there) must be of length `sequence_length`.
                    for n in range(min_freq - 1):
                        if (
                            i_str[n * sequence_length:(n + 1) * sequence_length] !=
                            i_str[(n + 1) * sequence_length:(n + 2) * sequence_length]
                        ):
                            break
                    else:
                        out.append(i)

    return out


def sum_invalid_ids(
        id_ranges: list[tuple[int, int]],
        invalid_ids_identifier: Callable[[tuple[int, int]], list[int]]
) -> int:
    out = 0
    for id_range in id_ranges:
        out += sum(invalid_ids_identifier(id_range))

    return out


if __name__ == "__main__":
    with open("../inputs/02.txt", "r") as fh:
        in_text = fh.read()

    ranges = parse_input(in_text)

    # PART 1
    start = time.perf_counter()
    res = sum_invalid_ids(ranges, get_invalid_ids_part1)
    end = time.perf_counter()
    print(f"Part 1 Result: {res}. Took {(end - start) * 1000:.2f} ms.")

    # PART 2
    start = time.perf_counter()
    res = sum_invalid_ids(ranges, get_invalid_ids_part2)
    end = time.perf_counter()
    print(f"Part 2 Result: {res}. Took {(end - start) * 1000:.2f} ms.")
