def merge(left: list[int], right: list[int]) -> list[int]:
    """
    Merge two sorted lists into one sorted list.
    This is the core combine step of Merge Sort.
    """
    result = []
    i = j = 0

    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1

    # Append any remaining elements
    result.extend(left[i:])
    result.extend(right[j:])
    return result


def merge_sort(data: list[int]) -> list[int]:
    """
    Recursively divide the list into halves, sort each half,
    then merge them back together.

    Time Complexity:  O(n log n) — best, average, and worst case
    Space Complexity: O(n)       — auxiliary space for merging
    """
    if len(data) <= 1:
        return data

    mid = len(data) // 2
    left  = merge_sort(data[:mid])
    right = merge_sort(data[mid:])

    return merge(left, right)


if __name__ == "__main__":
    import random
    import time

    sample = [random.randint(1, 1_000_000) for _ in range(10_000)]
    start = time.time()
    sorted_data = merge_sort(sample)
    elapsed = time.time() - start

    print(f"Sequential Merge Sort — 10,000 elements")
    print(f"  First 10 sorted: {sorted_data[:10]}")
    print(f"  Elapsed time:    {elapsed:.4f}s")
    print(f"  Correctly sorted: {sorted_data == sorted(sample)}")
