import time

EXAMPLE = """
L68
L30
R48
L5
R60
L55
L1
L99
R14
L82
"""


def parse_input(text: str) -> list[int]:
    instructions = text.strip().split("\n")
    increments = []
    for instruction in instructions:
        direction = instruction[0]
        amount = int(instruction[1:])
        if direction == "R":
            increments.append(amount)
        elif direction == "L":
            increments.append(-amount)
        else:
            raise ValueError(f"Unknown direction '{direction}'.")

    return increments


def get_zero_crossings_part1(increments: list[int]) -> int:
    counter = 0
    pos = 50
    for increment in increments:
        pos = (pos + increment) % 100
        if pos == 0:
            counter += 1

    return counter


def get_zero_crossings_part2(increments: list[int]) -> int:
    counter = 0
    pos = 50
    for increment in increments:
        target_pos = pos + increment
        counter += abs(target_pos // 100)

        # The above "target_pos // 100" logic counts whenever we cross the branch cut at <0.
        # Therefore, we must correct it in two edge cases:
        # i) When we already start on a zero and turn left, the counting logic counts this
        #    erroneously as a crossing of zero, so we need to fix it
        if pos == 0 and increment < 0:
            counter -= 1

        pos = target_pos % 100

        # ii) When we reach a zero from the right, i.e., from  positions > 0, the counting logic
        #     is not triggered, so we need to fix this, as well
        if pos == 0 and increment < 0:
            counter += 1

    return counter


if __name__ == "__main__":
    with open("../inputs/01.txt", "r") as fh:
        in_text = fh.read()

    increments_list = parse_input(in_text)

    # PART 1
    start = time.perf_counter()
    res = get_zero_crossings_part1(increments_list)
    end = time.perf_counter()
    print(f"Part 1 Result: {res}. Took {(end - start) * 1000:.2f} ms.")

    # PART 2
    start = time.perf_counter()
    res = get_zero_crossings_part2(increments_list)
    end = time.perf_counter()
    print(f"Part 2 Result: {res}. Took {(end - start) * 1000:.2f} ms.")
