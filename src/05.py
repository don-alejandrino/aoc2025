import time

EXAMPLE = """
3-5
10-14
16-20
12-18

1
5
8
11
17
32
"""


def parse_input(text: str) -> tuple[list[list[int]], list[int]]:
    ranges_block, id_block = text.strip().split("\n\n")
    ranges = [
        list(map(int, r.split("-"))) for r in ranges_block.strip().split("\n")
    ]
    ids = list(map(int, id_block.strip().split("\n")))

    return ranges, ids


def get_num_fresh_ids(ranges: list[list[int]], ids: list[int]) -> int:
    counter = 0
    for id_ in ids:
        if any([r[0] <= id_ <= r[1] for r in ranges]):
            counter += 1

    return counter


def get_id_ranges_without_overlaps(id_ranges: list[list[int]]) -> list[list[int]]:
    # For the following logic, we require the input ranges to be sorted in ascending order
    # according to their starting point
    id_ranges.sort(key=lambda x: x[0])
    merged_ranges = []
    for r in id_ranges:
        for i, mr in enumerate(merged_ranges):
            if r[0] > mr[1]:
                # |-----mr-----|
                #                  |---r---|
                # No overlap of the "new" range `r` with the current subset `mr` of the merged
                # ranges. `r` is right of `mr`, so directly jump to the next subset of the merged
                # ranges
                continue
            if mr[0] <= r[1] <= mr[1]:
                #  -----mr-----|
                #  --r----|
                # End point of `r` lies within `mr` => Simply extend `mr` to the left (the starting
                # point of `r` might be located left to the starting point of `mr`) and we're done
                mr[0] = min(r[0], mr[0])
                break
            elif r[1] > mr[1]:
                # If the end point of `r` is right of the end point of `mr`, we have the most
                # difficult case: `r` might extend into the next subset of `merged_ranges`.
                # In any case, update the starting point of `mr`first
                mr[0] = min(r[0], mr[0])
                if i == len(merged_ranges) - 1 or r[1] < merged_ranges[i + 1][0]:
                    # --merged_ranges[i]--|        |---merged_ranges[i + 1]--
                    # -----------r------------|
                    # No overlap with the next subset => simply extend `mr` to the right
                    mr[1] = r[1]
                    break
                else:
                    # --merged_ranges[i]--|        |---merged_ranges[i + 1]--
                    # ------------------r------------------------------------
                    #
                    #                              |
                    #                              V
                    #
                    # ------merged_ranges[i]------||---merged_ranges[i + 1]--
                    #                              |------------------r------
                    # Overlap with the next subset => Cut `r` at the overlap. `mr` is extended with
                    # the left side of this cut, while we continue the loop with the right side of
                    # the cut
                    mr[1] = merged_ranges[i + 1][0] - 1
                    r[0] = merged_ranges[i + 1][0]
        else:
            # No overlap of `r` with any subset of `merged_ranges`
            merged_ranges.append(r)

    return merged_ranges


def get_num_possible_ids(id_ranges: list[list[int]]) -> int:
    id_ranges_without_overlaps = get_id_ranges_without_overlaps(id_ranges)
    counter = 0
    for id_range in id_ranges_without_overlaps:
        counter += id_range[1] - id_range[0] + 1

    return counter


if __name__ == "__main__":
    with open("../inputs/05.txt", "r") as fh:
        in_text = fh.read()

    fresh_ingredient_ranges, ingredient_ids = parse_input(in_text)

    # PART 1
    start = time.perf_counter()
    res = get_num_fresh_ids(fresh_ingredient_ranges, ingredient_ids)
    end = time.perf_counter()
    print(f"Part 1 Result: {res}. Took {(end - start) * 1000:.2f} ms.")

    # PART 2
    start = time.perf_counter()
    res = get_num_possible_ids(fresh_ingredient_ranges)
    end = time.perf_counter()
    print(f"Part 2 Result: {res}. Took {(end - start) * 1000:.2f} ms.")
