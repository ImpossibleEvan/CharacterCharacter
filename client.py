from concurrent.futures import thread
import socket
import threading
import time

message = "" # thing sent
data = "" # thing received

def send(msg) -> None:
    global message
    message = msg

def check() -> str:
    global data
    return data

def myIP() -> str:
    hostname = socket.gethostname()
    ip = socket.gethostbyname(hostname)
    return ip

def main() -> None:
    global data, pdata, clientSocket

    while True:
        reply = message
        clientSocket.sendall(reply.encode())

        pdata = data
        data = clientSocket.recv(1024).decode()
        if not data:
            break

        time.sleep(0.01) 

    clientSocket.close()

def setup() -> None:
    global mainThread, clientSocket
    
    # Create a TCP/IP socket
    clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # Connect to the server (replace with the server's IP address)
    while True:
        try:
            clientSocket.connect((input("Enter server IP address: "), int(input("Enter server port: ") or "5000")))
            print("Connected to the server.")
            break
        except ConnectionRefusedError as e:
            print(f"Do not attempt connection until server is ready.")
            input("Press Enter to retry...")
        except Exception as e:
            print(f"Connection failed: {e}")
            input("Press Enter to retry...")

    # ^^^ Must happen before starting the thread ^^^

    mainThread = threading.Thread(target=main, daemon=True)
    mainThread.start()