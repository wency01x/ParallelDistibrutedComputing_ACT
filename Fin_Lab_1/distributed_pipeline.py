from mpi4py import MPI
from multiprocessing import Manager, Lock
import time
import random
import json
from datetime import datetime

def server_log(level: str, node: str, message: str):
    timestamp = datetime.now().strftime('%H:%M:%S.%f')[:-3]
    print(f"[{timestamp}] [{level.upper():<5}] [{node:<15}] {message}")

def generate_govtech_payloads() -> list:
    return [
        {"trace_id": "TXN-881", "type": "RBIM_SYNC", "payload": {"brgy": "Tagoloan", "records": 42}},
        {"trace_id": "TXN-882", "type": "GANAP_TABULATION", "payload": {"event": "Linggo ng Kabataan", "scores": 8}},
        {"trace_id": "TXN-883", "type": "DISASTER_ALERT", "payload": {"source": "PAGASA", "level": "Orange"}},
        {"trace_id": "TXN-884", "type": "CLEARANCE_REQ", "payload": {"user_id": "10045", "status": "Pending"}},
        {"trace_id": "TXN-885", "type": "GANAP_MEET_ENGINE", "payload": {"matchup": "A vs C", "bracket": "Semi"}},
        {"trace_id": "TXN-886", "type": "RBIM_MIGRANT_LOG", "payload": {"origin": "CDO", "dest": "Tagoloan"}},
    ]

def main():
    comm = MPI.COMM_WORLD
    rank = comm.Get_rank()
    size = comm.Get_size()

    manager = Manager()
    shared_data_lake = manager.list()
    ipc_write_lock = Lock()

    if rank == 0:
        node_name = "API-Gateway"
        server_log("INFO", node_name, "Booting Distributed Ingestion Pipeline...")
        
        workloads = generate_govtech_payloads()
        active_nodes = size - 1

        for i, payload in enumerate(workloads):
            target_node = (i % active_nodes) + 1
            packet = json.dumps(payload)
            comm.send(packet, dest=target_node, tag=100)
            server_log("DEBUG", node_name, f"Routed {payload['trace_id']} -> Worker Node {target_node}")

        for i in range(1, size):
            comm.send(None, dest=i, tag=100)

        aggregated_logs = []
        for i in range(1, size):
            node_results = comm.recv(source=i, tag=200)
            aggregated_logs.extend(node_results)

        print("\n" + "="*50)
        print(" 📊 SYSTEM STATE: SHARED MEMORY DATA LAKE")
        print("="*50)
        for record in aggregated_logs:
            print(f" ↳ {record}")
        print("="*50 + "\n")

    else:
        services = {1: "RBIM-Service", 2: "GANAP-Service", 3: "DisasterAPI"}
        node_name = services.get(rank, f"Service-{rank}")
        local_cache = []

        while True:
            raw_packet = comm.recv(source=0, tag=100)
            if raw_packet is None:
                server_log("INFO", node_name, "Received termination signal. Spinning down.")
                break 

            task = json.loads(raw_packet)
            server_log("INFO", node_name, f"Ingesting {task['type']} ({task['trace_id']})")
            
            db_latency = random.uniform(0.3, 1.8)
            time.sleep(db_latency)
            
            processed_state = f"{task['trace_id']} | TYPE: {task['type']} | LATENCY: {db_latency:.2f}s | NODE: {node_name}"
            
            with ipc_write_lock:
                shared_data_lake.append(processed_state)
                local_cache.append(processed_state)
                server_log("SUCCESS", node_name, f"Committed {task['trace_id']} to Shared Data Lake.")

        comm.send(local_cache, dest=0, tag=200)

if __name__ == "__main__":
    main()
