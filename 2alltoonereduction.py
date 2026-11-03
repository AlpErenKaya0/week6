from mpi4py import MPI

comm = MPI.COMM_WORLD
rank = comm.Get_rank()

# Her sürecin kendi sayısı var.
sayi = (rank + 1) * 10

print(f"Rank {rank}: benim sayım {sayi}")

# Bütün süreçlerin sayıları toplanır.
# Sonuç yalnızca rank 0'a verilir.
toplam = comm.reduce(sayi, op=MPI.SUM, root=0)

if rank == 0:
    print(f"İndirgeme sonucu: {toplam}")