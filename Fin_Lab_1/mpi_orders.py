from mpi4py import MPI

def main():
    comm = MPI.COMM_WORLD
    rank = comm.Get_rank()
    size = comm.Get_size()
    
    if rank == 0:
        print("Master (Rank 0): Generating customer orders...\n")
        orders = [
            {"id": "ORD-001", "item": "Laptop"},
            {"id": "ORD-002", "item": "Wireless Mouse"},
            {"id": "ORD-003", "item": "Mechanical Keyboard"},
            {"id": "ORD-004", "item": "27-inch Monitor"},
            {"id": "ORD-005", "item": "USB-C Hub"},
            {"id": "ORD-006", "item": "Webcam"}
        ]
        
        active_workers = size - 1
        for i, order in enumerate(orders):
            target = (i % active_workers) + 1
            comm.send(order, dest=target, tag=11)
            print(f"Master: Assigned {order['id']} to Worker {target}")
            
        for i in range(1, size):
            comm.send(None, dest=i, tag=11)
            
    else:
        pass # Workers will be implemented next

if __name__ == "__main__":
    main()
