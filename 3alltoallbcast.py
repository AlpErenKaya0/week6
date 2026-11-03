from mpi4py import MPI

comm = MPI.COMM_WORLD
rank = comm.Get_rank()

# Her sürecin kendi verisi.
sayi = (rank + 1) * 10

# Herkes kendi sayısını paylaşır.
# Herkes bütün sayıları alır.
tum_sayilar = comm.allgather(sayi)

print(
    f"Rank {rank}: benim sayım={sayi}, bütün sayılar={tum_sayilar}")