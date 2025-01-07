# import socket

# def scan_ports(ip):
#     for port in range(1, 1025):
#         sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#         sock.settimeout(0.5)
#         result = sock.connect_ex((ip, port))
#         if result == 0:
#             print(f"Port {port} is open")
#         sock.close()
        
# target_ip="192.168.29.1"
# scan_ports(target_ip)  # replace with your target IP address


import socket
import threading

def scan_port(ip, port):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(0.1)  # Réduire le timeout
        result = sock.connect_ex((ip, port))
        if result == 0:
            print(f"Port {port} is open")
        sock.close()
    except Exception as e:
        pass  # Ignorer les erreurs

def scan_ports(ip, start_port, end_port):
    threads = []
    for port in range(start_port, end_port + 1):
        thread = threading.Thread(target=scan_port, args=(ip, port))
        threads.append(thread)
        thread.start()

        # Limiter le nombre de threads actifs pour éviter la surcharge
        if len(threads) >= 100:
            for t in threads:
                t.join()  # Attendre que les threads actuels se terminent
            threads = []  # Réinitialiser la liste des threads
    # Attendre la fin des threads restants
    for t in threads:
        t.join()

if __name__ == "__main__":
    target_ip = "192.168.29.1"
    scan_ports(target_ip, 1, 1024)