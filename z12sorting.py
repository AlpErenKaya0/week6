from mpi4py import MPI
from heapq import merge
from collections import Counter
import random

comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()

PROCESS_COUNT = 4
ELEMENT_COUNT = 100
BLOCK_SIZE = ELEMENT_COUNT // PROCESS_COUNT

SOURCE_RANK = 0
OUTPUT_RANK = 3

if size != PROCESS_COUNT:
    if rank == SOURCE_RANK:
        print("Error: Run this program with exactly 4 processes.")
    comm.Abort(1)

# Rank 0 creates the input and prepares equal-sized blocks.
if rank == SOURCE_RANK:
    generator = random.Random(42)

    input_data = [
        generator.randint(1, 100)
        for _ in range(ELEMENT_COUNT)
    ]

    blocks = [
        input_data[start:start + BLOCK_SIZE]
        for start in range(0, ELEMENT_COUNT, BLOCK_SIZE)
    ]
else:
    blocks = None

# Every process receives 25 elements.
local_data = comm.scatter(blocks, root=SOURCE_RANK)

# Keep an input copy only for final correctness verification.
original_block = local_data.copy()

# Initial sorting is performed independently by each process.
local_data.sort()

history = [
    f"Rank {rank}: initial sorted block = {local_data}"
]

# Perform four odd-even compare-split phases.
for phase in range(PROCESS_COUNT):

    # Even phases: (0, 1), (2, 3)
    # Odd phases:  (1, 2)
    if phase % 2 == 0:
        partner = rank + 1 if rank % 2 == 0 else rank - 1
    else:
        partner = rank - 1 if rank % 2 == 0 else rank + 1

    if not 0 <= partner < size:
        history.append(
            f"Phase {phase + 1}, rank {rank}: no partner"
        )
        continue

    metadata_tag = 100 + phase
    data_tag = 200 + phase

    local_bounds = (local_data[0], local_data[-1])

    # Exchange only minimum and maximum values first.
    partner_bounds = comm.sendrecv(
        sendobj=local_bounds,
        dest=partner,
        sendtag=metadata_tag,
        source=partner,
        recvtag=metadata_tag
    )

    # Both partners make the same exchange decision.
    if rank < partner:
        exchange_needed = local_bounds[1] > partner_bounds[0]
    else:
        exchange_needed = partner_bounds[1] > local_bounds[0]

    if not exchange_needed:
        history.append(
            f"Phase {phase + 1}, rank {rank}: "
            f"partner={partner}, "
            f"local bounds={local_bounds}, "
            f"partner bounds={partner_bounds}, "
            f"data exchange skipped"
        )
        continue

    # Exchange the full sorted blocks only when necessary.
    partner_data = comm.sendrecv(
        sendobj=local_data,
        dest=partner,
        sendtag=data_tag,
        source=partner,
        recvtag=data_tag
    )

    # Merge two sorted blocks without sorting from scratch.
    combined_data = list(merge(local_data, partner_data))

    if rank < partner:
        local_data = combined_data[:BLOCK_SIZE]
    else:
        local_data = combined_data[-BLOCK_SIZE:]

    history.append(
        f"Phase {phase + 1}, rank {rank}: "
        f"partner={partner}, "
        f"new block={local_data}"
    )

    # Temporary copies are no longer needed.
    del partner_data
    del combined_data

# Gather final blocks and diagnostic information at rank 3.
report = {
    "rank": rank,
    "original_block": original_block,
    "sorted_block": local_data,
    "history": history
}

reports = comm.gather(report, root=OUTPUT_RANK)

if rank == OUTPUT_RANK:
    original_data = [
        value
        for report in reports
        for value in report["original_block"]
    ]

    # Rank order is already the global sorted block order.
    final_data = [
        value
        for report in reports
        for value in report["sorted_block"]
    ]

    print("--- Original Input ---")
    print(original_data)

    print("\n--- Communication History ---")
    for report in reports:
        for entry in report["history"]:
            print(entry)

    print("\n--- Final Block Ownership ---")
    for report in reports:
        owner = report["rank"]
        start = owner * BLOCK_SIZE
        end = start + BLOCK_SIZE - 1

        print(
            f"Rank {owner}: global indices {start}-{end}, "
            f"block={report['sorted_block']}"
        )

    is_sorted = all(
        final_data[index] <= final_data[index + 1]
        for index in range(len(final_data) - 1)
    )

    same_values = Counter(original_data) == Counter(final_data)

    print("\n--- Final Sorted List: Rank 3 ---")
    print(final_data)

    print("\n--- Verification ---")
    print(f"Element count: {len(final_data)}")
    print(f"Sorted correctly: {is_sorted}")
    print(f"Original values preserved: {same_values}")

    assert len(final_data) == ELEMENT_COUNT
    assert is_sorted
    assert same_values