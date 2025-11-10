import socket
import threading
from typing import Optional

"""
This module provides a simple implementation of a two-way communication.
One person can type a message and it will be immediately printed into the other person's console.
Neither person is a host or a client; both run the same code.
"""

def attempt_connection(host, port) -> Optional[socket.socket]:
    """Try to connect to the given host and port."""
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        s.connect((host, port))
        return s
    except ConnectionRefusedError:
        s.close()
        return None

def check_incoming_data(conn: socket.socket):
    """Check for incoming data and print it to the console."""
    while True:
        try:
            data = conn.recv(1024)
        except OSError:
            break
        if not data:
            break
        print("\nReceived:", data.decode())

def send_outgoing_data(conn: socket.socket):
    """Read user input and send it to the connected peer."""
    while True:
        message = input("Enter message: ")
        conn.sendall(message.encode())

def start_two_way_communication(host: str, port: int):
    """Start the two-way communication."""
    conn = attempt_connection(host, port)
    if conn is None:
        # Act as server
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.bind((host, port))
        server_socket.listen(1)
        print("Waiting for incoming connection...")
        conn, _ = server_socket.accept()
        print("Connection established.")
    # Start threads for sending and receiving data
    threading.Thread(target=send_outgoing_data, args=(conn,), daemon=True).start()
    threading.Thread(target=check_incoming_data, args=(conn,), daemon=True).start()
    # Start threads for sending and receiving data
    # Keep the main thread alive
    try:
        while True:
            # sleep/wait to avoid busy-waiting
            threading.Event().wait(1)
    except KeyboardInterrupt:
        print("Shutting down.")
        try:
            conn.close()
        except Exception:
            pass
        try:
            server_socket.close()
        except Exception:
            pass
    # Keep the main thread alive
    while True:
        pass

if __name__ == "__main__":
    # Print out own IP address and port
    try:
        local_ip = socket.gethostbyname(socket.gethostname())
        print(f"Your IP address is {local_ip}. Share this with the other person.")
        other_host = input("Enter the other person's IP address (or leave blank for localhost): ")
        other_port = input("Enter the port number to use (default 5000): ")
        HOST = other_host if other_host else "localhost"
        PORT = int(other_port) if other_port else 5000
        start_two_way_communication(HOST, PORT)
    except Exception as e:
        print("An error occurred:", e)
    except KeyboardInterrupt:
        print("Exiting program.")
    finally:
        input("Press Enter to close...")