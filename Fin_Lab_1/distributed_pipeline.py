from mpi4py import MPI
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
    else:
        pass

if __name__ == "__main__":
    main()
