import socket

# Create a TCP/IP socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind the socket to an IP and port
server_socket.bind(('0.0.0.0', 5000))
server_socket.listen(1)

# Print IP for others
hostname = socket.gethostname()
ip_address = socket.gethostbyname(hostname)
print(f"Server IP address: {ip_address}")

print("Server listening on port 5000...")

# Wait for a connection
conn, addr = server_socket.accept()
print(f"Connected by {addr}")

while True:
    data = conn.recv(1024).decode()
    if not data:
        break
    print(f"Client: {data}")

    # Send a reply back to the client
    reply = input("Server: ")
    conn.sendall(reply.encode())

conn.close()
