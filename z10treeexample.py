from mpi4py import MPI

comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()

# Each process starts with its own value.
value = (rank + 1) * 10
subtotal = value

# Determine the children of this process.
left_child = 2 * rank + 1
right_child = 2 * rank + 2

# Receive the subtotal from the left child, if it exists.
if left_child < size:
    received_value = comm.recv(source=left_child)
    subtotal += received_value

# Receive the subtotal from the right child, if it exists.
if right_child < size:
    received_value = comm.recv(source=right_child)
    subtotal += received_value

if rank != 0:
    # Every non-root process sends its subtotal to its parent.
    parent = (rank - 1) // 2
    comm.send(subtotal, dest=parent)

    print(
        f"Rank {rank}: subtree sum={subtotal}, "
        f"parent={parent}"
    )
else:
    print(f"Rank 0: total sum={subtotal}")