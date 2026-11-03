from mpi4py import MPI

comm = MPI.COMM_WORLD
rank = comm.Get_rank()

# Her sürecin kendi verisi.
sayi = (rank + 1) * 10

# Herkes kendi verisini rank 0'da toplar.
toplanan_veriler = comm.gather(sayi, root=0)

if rank == 0:
    print("Toplanan veriler:", toplanan_veriler)