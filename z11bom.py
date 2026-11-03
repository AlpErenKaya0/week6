from mpi4py import MPI

comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()

PLAYER_COUNT = 9
COUNTER_RANK = 9
LIMIT = 90

TOKEN_TAG = 1
REPORT_TAG = 2

if size != PLAYER_COUNT + 1:
    if rank == 0:
        print("Error: Run this program with exactly 10 processes.")
    comm.Abort(1)

if rank < PLAYER_COUNT:
    bom_count = 0

    previous_player = (rank - 1) % PLAYER_COUNT
    next_player = (rank + 1) % PLAYER_COUNT

    # Each player handles its own turns.
    for turn in range(rank + 1, LIMIT + 1, PLAYER_COUNT):

        # Rank 0 starts the game without receiving a token.
        if turn == 1:
            number = 1
        else:
            number = comm.recv(
                source=previous_player,
                tag=TOKEN_TAG
            )

        if number % 5 == 0:
            bom_count += 1
            print(
                f"Rank {rank}: BOM "
                f"(number={number}, count={bom_count})",
                flush=True
            )
        else:
            print(f"Rank {rank}: {number}", flush=True)

        # Pass the next number unless the game has ended.
        if number < LIMIT:
            comm.send(
                number + 1,
                dest=next_player,
                tag=TOKEN_TAG
            )

    # Send the player's final report to the counter.
    report = {
        "rank": rank,
        "bom_count": bom_count
    }

    comm.send(
        report,
        dest=COUNTER_RANK,
        tag=REPORT_TAG
    )

else:
    reports = {}

    # Collect one final report from each player.
    for _ in range(PLAYER_COUNT):
        report = comm.recv(
            source=MPI.ANY_SOURCE,
            tag=REPORT_TAG
        )

        reports[report["rank"]] = report["bom_count"]

    print("\n--- Final BOM Report ---", )

    for player_rank in sorted(reports):
        print(
            f"Player rank {player_rank}: "
            f"BOM count = {reports[player_rank]}", 
        )

    print(
        f"Total BOM count = {sum(reports.values())}",
    )