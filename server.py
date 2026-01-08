import socket
import time
import requests

message = "" # thing sent
data = "" # thing received
pdata = "" # previous thing received

def send(msg) -> None:
    global message
    message = msg

def check() -> str:
    global data
    return data

def uniqueCheck() -> str:
    global data, pdata
    return data if data != pdata else ""

def main() -> None:
    global data, pdata
    # Create a TCP/IP socket
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Bind the socket to an IP and port
    server_socket.bind(('0.0.0.0', 5000))
    server_socket.listen(1)

    # Print IP for others
    hostname = socket.gethostname()
    ip_address = socket.gethostbyname(hostname)
    
    public_ip = requests.get("https://api.ipify.org").text
    print(f"LAN IP address: {ip_address}")
    print(f"Public IP address: {public_ip}")

    print("Server listening on port 5000...")

    # Wait for a connection
    conn, addr = server_socket.accept()
    print(f"Connected by {addr}")

    while True:
        data = conn.recv(1024).decode()
        if not data:
            break
        
        pdata = data
        reply = message
        conn.sendall(reply.encode())
        time.sleep(0.01) 

    conn.close()

if __name__ == "__main__":
    main()