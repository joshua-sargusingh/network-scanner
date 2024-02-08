import socket
import threading

def syn_scan_target(ip, port):
    try:
        # Create a socket object
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # Set a timeout for the connection attempt
        s.settimeout(1)
        
        # Send a SYN packet to the target IP and port
        s.connect_ex((ip, port))
        # If successful, print the open port
        print(f"[+] {ip}:{port} is open")
        # Close the socket
        s.close()

    except (socket.timeout, socket.error):
        pass

def syn_scan(ip, ports):
    print(f"Scanning {ip} ...")
    for port in ports:
        threading.Thread(target=syn_scan_target, args = (ip, port)).start()

def main():
    target_ip = "127.0.0.1"
    target_ports = range(1,100)
    
    syn_scan(target_ip, target_ports)

if __name__ == "__main__":
    main()