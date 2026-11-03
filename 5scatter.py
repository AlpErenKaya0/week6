from mpi4py import MPI

comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()

if size != 4:
    if rank == 0:
        print("Bu örneği tam 4 süreçle çalıştır.")

else:
    if rank == 0:
        veriler = [10, 20, 30, 40]
    else:
        veriler = None

    # Her süreç kendisine düşen elemanı alır.
    benim_verim = comm.scatter(veriler, root=0)

    print(f"Rank {rank}: aldığım veri = {benim_verim}")