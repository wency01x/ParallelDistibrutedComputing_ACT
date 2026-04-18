#seq

def linear_search(data: list[int], target: int) -> int:
    """
    Scan the list from left to right, returning the index of the first
    occurrence of target, or -1 if not found.

    Time Complexity:  O(n) — worst and average case (target near end or absent)
                      O(1) — best case (target at index 0)
    Space Complexity: O(1) — no extra data structures
    """
    for index, value in enumerate(data):
        if value == target:
            return index
    return -1


def linear_search_all(data: list[int], target: int) -> list[int]:
    """
    Return ALL indices where target appears in data.
    Useful for datasets that may contain duplicates.
    """
    return [index for index, value in enumerate(data) if value == target]


if __name__ == "__main__":
    import random
    import time

    data   = [random.randint(1, 1_000_000) for _ in range(100_000)]
    target = data[random.randint(0, len(data) - 1)]  # guaranteed hit

    start  = time.time()
    result = linear_search(data, target)
    elapsed = time.time() - start

    print(f"Sequential Linear Search — 100,000 elements")
    print(f"  Target: {target}")
    print(f"  Found at index: {result}")
    print(f"  Elapsed time:   {elapsed:.6f}s")

    # Also test a miss
    miss_result = linear_search(data, -1)
    print(f"  Search for -1 (not in list): index = {miss_result}")
