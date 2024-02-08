import socket
import threading

def scan_target(ip, port):
    try:
        # Create a socket object
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # Set a timeout for the connection attempt
        s.settimeout(1)
        # Attempt to connect to the target IP and port
        s.connect((ip, port))
        # If successful, print the open port
        print(f"[+] {ip}:{port} is open")
        # Close the socket 
        s.close()
    except (socket.timeout, socket.error):
        pass

def tcp_scan(ip, ports):
    print(f"Scanning {ip}...")
    for port in ports:
        # Create a thread for each port scan to speed up the process
        threading.Thread(target=scan_target, args=(ip, port)).start()

def main():
    # Specify the target IP address and range of ports to scan
    target_ip = "127.0.0.1"
    target_ports = range(1, 1025)  # Scan ports from 1 to 1024

    # Start the scan
    tcp_scan(target_ip, target_ports)

if __name__ == "__main__":
    main()