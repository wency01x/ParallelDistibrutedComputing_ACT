from mpi4py import MPI
import time
import random

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
            
        for i in range(1, size):
            comm.send(None, dest=i, tag=11)
            
    else:
        while True:
            order = comm.recv(source=0, tag=11)
            if order is None:
                break
                
            print(f"Worker {rank}: Received {order['id']} ({order['item']})")
            
            # Simulate real-world processing delay
            delay = random.uniform(0.5, 2.0)
            time.sleep(delay)
            
            print(f"Worker {rank}: Finished {order['id']} in {delay:.2f}s")

if __name__ == "__main__":
    main()
