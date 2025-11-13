import socket
import time

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
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Connect to the server (replace with the server's IP address)
    client_socket.connect((input("Enter server IP address: "), int("5000" or input("Enter server port: "))))

    print("Connected to the server.")

    while True:
        reply = message
        client_socket.sendall(reply.encode())

        pdata = data
        data = client_socket.recv(1024).decode()
        if not data:
            break

        time.sleep(0.01) 

    client_socket.close()

if __name__ == "__main__":
    main()