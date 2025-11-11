try:
    import argparse
    import socket
    import threading
    import sys

    #!/usr/bin/env python3
    """
    Simple two-way chat for two computers.
    Run one side as server: python chat.py --listen --port 5000
    Run the other side as client: python chat.py --connect HOST --port 5000
    Type messages and press Enter to send. Use /quit or Ctrl+C to exit.
    """


    def recv_loop(sock):
        try:
            while True:
                data = sock.recv(4096)
                if not data:
                    print("\n[remote disconnected]")
                    try:
                        sock.close()
                    finally:
                        sys.exit(0)
                print("\nremote: " + data.decode(errors="replace"))
        except Exception:
            sys.exit(0)

    def send_loop(sock):
        try:
            while True:
                line = input()
                if not line:
                    continue
                if line.strip().lower() in ("/quit", "quit", "exit"):
                    try:
                        sock.shutdown(socket.SHUT_RDWR)
                    except Exception:
                        pass
                    sock.close()
                    sys.exit(0)
                try:
                    sock.sendall(line.encode())
                except Exception:
                    print("Failed to send. Connection may be closed.")
                    sys.exit(0)
        except (KeyboardInterrupt, EOFError):
            try:
                sock.shutdown(socket.SHUT_RDWR)
            except Exception:
                pass
            sock.close()
            sys.exit(0)

    def start_server(port):
        srv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        srv.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        srv.bind(("0.0.0.0", port))
        srv.listen(1)
        print(f"Listening on 0.0.0.0:{port} ... waiting for connection")
        conn, addr = srv.accept()
        print(f"Connected by {addr[0]}:{addr[1]}")
        srv.close()
        return conn

    def start_client(host, port):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((host, port))
        print(f"Connected to {host}:{port}")
        return sock

    def main():
        parser = argparse.ArgumentParser()
        group = parser.add_mutually_exclusive_group()
        group.add_argument("--listen", action="store_true", help="Run as server (accept one connection)")
        group.add_argument("--connect", metavar="HOST", help="Connect to server at HOST")
        parser.add_argument("--port", type=int, default=5000, help="Port (default 5000)")
        
        if len(sys.argv) > 1:
            args = parser.parse_args()
        else:
            # Interactive mode if no arguments are provided
            args = argparse.Namespace(listen=False, connect=None, port=5000)
            choice = input("Run as (s)erver or (c)lient? ").lower()
            if choice.startswith('s'):
                args.listen = True
                port_str = input(f"Enter port to listen on (default {args.port}): ")
                if port_str:
                    args.port = int(port_str)
            elif choice.startswith('c'):
                args.connect = input("Enter host to connect to: ")
                if not args.connect:
                    print("Host is required.")
                    return
                port_str = input(f"Enter port (default {args.port}): ")
                if port_str:
                    args.port = int(port_str)
            else:
                print("Invalid choice.")
                return

        if args.listen:
            sock = start_server(args.port)
        elif args.connect:
            sock = start_client(args.connect, args.port)
        else:
            parser.print_help()
            return

        t = threading.Thread(target=recv_loop, args=(sock,), daemon=True)
        t.start()
        print("You can start typing messages. Type /quit to exit.")
        send_loop(sock)

    if __name__ == "__main__":
        try:
            main()
        except SystemExit as e:
            # Argparse calls sys.exit() on error, which raises SystemExit.
            # We can ignore it or handle it if we want to prevent exit.
            # In this case, we let it proceed to finally.
            pass
except Exception as e:
    print(f"An error occurred: {e}")
finally:
    input("Press Enter to exit...")