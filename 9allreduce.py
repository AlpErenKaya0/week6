from mpi4py import MPI

comm = MPI.COMM_WORLD
rank = comm.Get_rank()

#Her sürecin kendi sayısı.
sayi =(rank + 1) * 10

# Bütün sayıları topla ve sonucu herkese ver.
genel_toplam = comm.allreduce(sayi, op=MPI.SUM)

print(
    f"Rank {rank}: kendi sayım={sayi}, "
    f"genel toplam={genel_toplam}"
)