from mpi4py import MPI

comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()

veri = (rank + 1) * 10

# Son rank'ten sonra tekrar rank 0'a dön.
hedef = (rank + 1) % size

# Rank 0'ın önceki komşusu son rank'tir.
kaynak = (rank - 1) % size

yeni_veri = comm.sendrecv(
    veri,
    dest=hedef,
    source=kaynak
)

print(
    f"Rank {rank}: eski veri={veri}, "
    f"yeni veri={yeni_veri}"
)