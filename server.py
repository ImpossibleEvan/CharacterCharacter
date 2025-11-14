import socket
import threading
import time

messages:dict[tuple, str] = {}
received:dict[tuple, str] = {}
clients:dict[tuple, socket.socket] = {}

def send(msg, addr:tuple[str, int]) -> None:
    global messages
    messages[addr] = msg

def sendAll(msg) -> None:
    global messages
    for ip in clients.keys():
        messages[ip] = msg

def check(ip) -> str:
    global received
    return received.get(ip, "")

def checkAll() -> dict[str, str]:
    global received
    return received

def myIP() -> str:
    hostname = socket.gethostname()
    ip = socket.gethostbyname(hostname)
    return ip

def setup() -> None:
    global serverSocket, listenThread, sendingThread, welcomeThread
    # Create a TCP/IP socket
    serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Bind the socket to an IP and port
    serverSocket.bind(('0.0.0.0', int(input("Enter server port: ") or "5000")))
    serverSocket.listen(1)

    # Print IP for others
    hostname = socket.gethostname()
    ip = socket.gethostbyname(hostname)
    print(f"Server IP address: {ip}")

    listenThread = threading.Thread(target=listen, daemon=True)
    listenThread.start()

    sendingThread = threading.Thread(target=sending, daemon=True)
    sendingThread.start()

    welcomeThread = threading.Thread(target=welcome, daemon=True)
    welcomeThread.start()

def welcome() -> None:
    global serverSocket, clients, messages
    while True:
        time.sleep(1)
        conn, addr = serverSocket.accept()
        print(f"Connected by {addr}")
        clients[addr] = conn
        messages[addr] = ""  # Initialize message for the new client

def listen() -> None:
    global received, clients
    
    while True:
        for addr, conn in list(clients.items()):  # iterate a snapshot to allow deletions
            time.sleep(0.01)
            try:
                data = conn.recv(1024)
            except socket.timeout:
                # No data received within timeout, just go to next guy
                continue
            except BlockingIOError:
                # If no data is available right now, just go to next guy
                continue
            except OSError:
                # The connection was closed, and we must clean it up
                conn.close()
                del clients[addr]
                continue

            if data:
                received[addr] = data.decode()
            else:
                conn.close()
                del clients[addr]

def sending() -> None:
    global messages, clients
    while True: # Lwk forgot this loop needed to be here and tried to fix nothing for about an hour
        time.sleep(0.01)
        for addr, conn in clients.items():
            # Get the message for this client and send it
            msg = messages[addr]
            try:
                # Send the message
                conn.sendall(msg.encode())
            except OSError:
                # The connection was closed, and we must clean it up
                conn.close()
                del clients[addr]
                continue # Go to the next client