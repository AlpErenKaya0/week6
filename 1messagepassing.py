from mpi4py import MPI
comm = MPI.COMM_WORLD
rank = comm.Get_rank()  # this is the process number. Bu sürecin numarası

if comm.Get_size() != 2:
    if rank == 0:
        print("This program works with exact 2 processes.")
else:
    if rank == 0:
        message = "hi! i'm process 0 "
        comm.send(message, dest=1)

    elif rank == 1:
        incoming_message = comm.recv(source=0)
        print("Process 1 took the message:", incoming_message)