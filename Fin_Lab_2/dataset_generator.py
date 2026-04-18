import random

# Generate a list of n random integers between 1 and 1,000,000.
def generate_random(n: int) -> list[int]:
    return [random.randint(1, 1_000_000) for _ in range(n)]

# Generate an already-sorted list of n integers (special case).
def generate_sorted(n: int) -> list[int]:
    return sorted(generate_random(n))

# Generate a reverse-sorted list of n integers (special case).
def generate_reverse_sorted(n: int) -> list[int]:
    return sorted(generate_random(n), reverse=True)


# Dataset sizes as specified in the act
SMALL  = 1_000
MEDIUM = 100_000
LARGE  = 1_000_000

DATASET_SIZES = {
    "small":   SMALL,
    "medium":  MEDIUM,
    "large":   LARGE,
}

if __name__ == "__main__":
    for label, size in DATASET_SIZES.items():
        data = generate_random(size)
        print(f"[{label.upper()}] Generated {len(data):,} elements | "
              f"Sample: {data[:5]} ...")
