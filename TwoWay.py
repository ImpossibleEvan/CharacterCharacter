import socket
import threading
from typing import Optional

"""
This module provides a simple implementation of a two-way communication.
One person can type a message and it will be immediately printed into the other person's console.
Neither person is a host or a client; both run the same code.
"""

def get_local_ip() -> str:
    """Return a likely external-facing local IP address (falls back to 127.0.0.1)."""
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        # This does not actually send data, but forces the OS to select a source IP.
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
    except Exception:
        ip = "127.0.0.1"
    finally:
        s.close()
    return ip

def attempt_connection(host, port) -> Optional[socket.socket]:
    """Try to connect to the given host and port."""
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        s.connect((host, port))
        return s
    except (ConnectionRefusedError, OSError):
        s.close()
        return None

def check_incoming_data(conn: socket.socket):
    """Check for incoming data and print it to the console."""
    try:
        while True:
            try:
                data = conn.recv(1024)
            except OSError:
                break
            if not data:
                print("\nConnection closed by peer.")
                break
            print("\nReceived:", data.decode())
    finally:
        try:
            conn.close()
        except Exception:
            pass

def send_outgoing_data(conn: socket.socket):
    """Read user input and send it to the connected peer."""
    try:
        while True:
            try:
                message = input("Enter message: ")
            except EOFError:
                # input closed; stop
                break
            if not message:
                continue
            try:
                conn.sendall(message.encode())
            except OSError:
                print("Failed to send message; connection may be closed.")
                break
    finally:
        try:
            conn.close()
        except Exception:
            pass

def start_two_way_communication(peer_host: Optional[str], port: int):
    """Start the two-way communication. If peer_host is provided, try to connect first; otherwise act as server."""
    conn = None
    if peer_host:
        conn = attempt_connection(peer_host, port)
    server_socket = None
    if conn is None:
        # Act as server and listen on all interfaces so other devices can connect
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server_socket.bind(("0.0.0.0", port))
        server_socket.listen(1)
        print(f"Waiting for incoming connection on port {port}...")
        try:
            conn, addr = server_socket.accept()
            print("Connection established with", addr)
        except Exception as e:
            print("Failed to accept connection:", e)
            server_socket.close()
            return

    # Start threads for sending and receiving data
    send_thread = threading.Thread(target=send_outgoing_data, args=(conn,), daemon=True)
    recv_thread = threading.Thread(target=check_incoming_data, args=(conn,), daemon=True)
    send_thread.start()
    recv_thread.start()

    try:
        # Wait for threads to finish (they will end when connection closes or on error)
        send_thread.join()
        recv_thread.join()
    except KeyboardInterrupt:
        print("Shutting down.")
        try:
            conn.close()
        except Exception:
            pass
    finally:
        if server_socket is not None:
            try:
                server_socket.close()
            except Exception:
                pass

if __name__ == "__main__":
    # Print out own IP address and port
    try:
        local_ip = get_local_ip()
        print(f"Your IP address is {local_ip}. Share this with the other person.")
        other_host = input("Enter the other person's IP address (leave blank to wait for an incoming connection): ").strip()
        other_port = input("Enter the port number to use (default 5000): ").strip()
        peer = other_host if other_host else None
        PORT = int(other_port) if other_port else 5000
        start_two_way_communication(peer, PORT)
    except KeyboardInterrupt:
        print("Exiting program.")
    except Exception as e:
        print("An error occurred:", e)
    finally:
        try:
            input("Press Enter to close...")
        except Exception:
            pass