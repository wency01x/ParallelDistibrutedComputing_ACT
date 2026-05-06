from mpi4py import MPI
from multiprocessing import Manager, Lock
import time
import random

def main():
    comm = MPI.COMM_WORLD
    rank = comm.Get_rank()
    size = comm.Get_size()
    
    # Initialize shared memory and synchronization tools
    manager = Manager()
    shared_orders = manager.list()
    lock = Lock()
    
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
            
        # Collect results to guarantee output printing in isolated MPI nodes
        final_orders = []
        for i in range(1, size):
            results = comm.recv(source=i, tag=22)
            final_orders.extend(results)
            
        print("\n--- MASTER: COMPLETE LIST OF PROCESSED ORDERS ---")
        for res in final_orders:
            print(f"✔️ {res}")
            
    else:
        local_results = []
        while True:
            order = comm.recv(source=0, tag=11)
            if order is None:
                break
                
            print(f"Worker {rank}: Received {order['id']} ({order['item']})")
            
            delay = random.uniform(0.5, 2.0)
            time.sleep(delay)
            
            result_string = f"Order {order['id']} ({order['item']}) handled by Worker {rank}"
            
            # Critical Section for writing shared orders
            with lock:
                shared_orders.append(result_string)
                local_results.append(result_string)
                
        comm.send(local_results, dest=0, tag=22)

if __name__ == "__main__":
    main()
