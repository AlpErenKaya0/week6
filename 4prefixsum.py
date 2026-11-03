from mpi4py import MPI

comm = MPI.COMM_WORLD
rank = comm.Get_rank()

# Her sürecin kendi sayısı.
sayi = (rank + 1) * 10

# Rank 0'dan bu sürece kadar olan değerleri topla.
onek_toplami = comm.scan(sayi, op=MPI.SUM)

print(
    f"Rank {rank}: kendi sayım={sayi}, önek toplamım={onek_toplami}"
)