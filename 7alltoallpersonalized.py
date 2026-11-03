from mpi4py import MPI

comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()

# Listenin her elemanı farklı bir hedef süreç içindir.
gonderilecek = []

for hedef in range(size):
    gonderilecek.append(rank * 10 + hedef)

# Her süreç, herkese kendisi için hazırlanmış elemanı yollar.
alinan = comm.alltoall(gonderilecek)

print(f"Rank {rank}: gönderilen={gonderilecek}, alınan={alinan}")