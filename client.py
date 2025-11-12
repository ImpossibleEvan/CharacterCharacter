import socket

def main():
    # Create a TCP/IP socket
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Connect to the server (replace with the server's IP address)
    client_socket.connect((input("Enter server IP address: "), int("5000" or input("Enter server port: "))))

    print("Connected to the server.")

    while True:
        message = input("Client: ")
        client_socket.sendall(message.encode())

        data = client_socket.recv(1024).decode()
        if not data:
            break
        print(f"Server: {data}")

    client_socket.close()

if __name__ == "__main__":
    main()