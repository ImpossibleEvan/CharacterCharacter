try:
    import argparse
    import socket
    import threading
    import sys
    import time

    #!/usr/bin/env python3
    """
    Simple multi-player Hangman game.
    Run one side as server: python 2way.py --listen --port 5000
    Run clients as: python 2way.py --connect HOST --port 5000
    The server chooses a word, clients guess. Use Ctrl+C to exit.
    """

    # --- Game Assets ---
    HANGMAN_PICS = ['''
      +---+
      |   |
          |
          |
          |
          |
    =========''', '''
      +---+
      |   |
      O   |
          |
          |
          |
    =========''', '''
      +---+
      |   |
      O   |
      |   |
          |
          |
    =========''', '''
      +---+
      |   |
      O   |
     /|   |
          |
          |
    =========''', '''
      +---+
      |   |
      O   |
     /|\\  |
          |
          |
    =========''', '''
      +---+
      |   |
      O   |
     /|\\  |
     /    |
          |
    =========''', '''
      +---+
      |   |
      O   |
     /|\\  |
     / \\  |
          |
    =========''']

    # --- Game Logic Class ---
    class Game:
        def __init__(self, word):
            self.word = word.lower().strip()
            self.guessed_letters = set()
            self.tries = 6
            self.game_over = False
            self.winner = None
            self.lock = threading.Lock()

        def get_state_string(self):
            """Constructs the display string for the current game state."""
            with self.lock:
                if self.game_over:
                    if self.winner:
                        return f"END:The word was '{self.word}'. {self.winner} won the game!"
                    else:
                        return f"END:Game Over! The word was: {self.word}"

                display = HANGMAN_PICS[6 - self.tries]
                
                word_display = " ".join([letter if letter in self.guessed_letters else "_" for letter in self.word])
                
                guessed_str = "Guessed letters: " + " ".join(sorted(list(self.guessed_letters)))
                
                return f"STATE:{display}\n\nWord: {word_display}\n{guessed_str}\nTries left: {self.tries}"

        def guess(self, letter, player_name):
            """Processes a guess and returns a message about the outcome."""
            with self.lock:
                if self.game_over:
                    return None # Game is already over

                letter = letter.lower()
                if not letter.isalpha() or len(letter) != 1:
                    return f"MSG:{player_name} made an invalid guess: '{letter}'"

                if letter in self.guessed_letters:
                    return f"MSG:{player_name} guessed '{letter}', which was already tried."
                
                self.guessed_letters.add(letter)

                if letter in self.word:
                    # Check for win
                    if all(char in self.guessed_letters for char in self.word):
                        self.game_over = True
                        self.winner = player_name
                    return f"MSG:Correct! {player_name} guessed '{letter}'."
                else:
                    self.tries -= 1
                    # Check for loss
                    if self.tries == 0:
                        self.game_over = True
                    return f"MSG:Incorrect! {player_name} guessed '{letter}'."

    # --- Server-side Code ---
    class Server:
        def __init__(self, port):
            self.clients = {} # conn -> name
            self.game = None
            self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.server_socket.bind(("0.0.0.0", port))
            self.port = port

        def broadcast(self, message):
            """Send a message to all connected clients."""
            print(f"[BROADCAST] {message.splitlines()[0]}")
            for conn in self.clients:
                try:
                    conn.sendall(message.encode())
                except socket.error:
                    # Client likely disconnected, will be removed in handler
                    pass

        def handle_client(self, conn, addr):
            """Thread function to handle a single client."""
            try:
                conn.sendall("NAME:".encode())
                name = conn.recv(1024).decode().strip()
                if not name:
                    name = f"Player_{addr[1]}"
                
                self.clients[conn] = name
                print(f"[CONNECT] {name} ({addr[0]}:{addr[1]}) has joined.")
                self.broadcast(f"MSG:{name} has joined the game!")
                time.sleep(0.1) # Give client time to process join message
                
                # Send current game state to new player
                if self.game:
                    conn.sendall(self.game.get_state_string().encode())

                while self.game and not self.game.game_over:
                    data = conn.recv(1024)
                    if not data:
                        break
                    
                    guess_letter = data.decode().strip()
                    
                    # Process guess and get message
                    guess_result_msg = self.game.guess(guess_letter, name)
                    
                    if guess_result_msg:
                        self.broadcast(guess_result_msg)
                        time.sleep(0.1) # Prevent messages from sticking together
                        self.broadcast(self.game.get_state_string())

            except (ConnectionResetError, ConnectionAbortedError):
                pass # Client disconnected abruptly
            finally:
                if conn in self.clients:
                    name = self.clients[conn]
                    del self.clients[conn]
                    print(f"[DISCONNECT] {name} has left.")
                    if self.game and not self.game.game_over:
                        self.broadcast(f"MSG:{name} has left the game.")
                conn.close()

        def run(self):
            """Main server loop."""
            self.server_socket.listen()
            print(f"Hangman server listening on 0.0.0.0:{self.port}...")

            # Thread to accept new connections
            threading.Thread(target=self.accept_connections, daemon=True).start()

            # Wait for at least one player to start
            while not self.clients:
                print("Waiting for the first player to connect...")
                time.sleep(2)

            word = input("Enter the word to be guessed: ").lower().strip()
            self.game = Game(word)
            print(f"Game started. The word is '{self.game.word}'. Broadcasting to players.")
            
            self.broadcast(self.game.get_state_string())

            # Wait for game to end
            while not self.game.game_over:
                time.sleep(1)
            
            print("Game has ended.")
            # Final state is broadcasted when game ends
            time.sleep(5) # Keep server alive for a bit to send final message
            self.server_socket.close()

        def accept_connections(self):
            while True:
                try:
                    conn, addr = self.server_socket.accept()
                    threading.Thread(target=self.handle_client, args=(conn, addr), daemon=True).start()
                except OSError: # Socket closed
                    break

    # --- Client-side Code ---
    def run_client_game(sock):
        """Client-side game loop."""
        try:
            while True:
                data = sock.recv(4096).decode()
                if not data:
                    print("\n[Server disconnected]")
                    break

                # Handle different message types from server
                if data.startswith("NAME:"):
                    name = input("Enter your name: ")
                    sock.sendall(name.encode())
                elif data.startswith("STATE:"):
                    print("\n" + "="*30)
                    print(data[len("STATE:"):])
                    guess = input("Enter your guess (a single letter): ")
                    if not guess:
                        guess = " " # Send something to avoid blocking
                    sock.sendall(guess[0].encode())
                elif data.startswith("MSG:"):
                    print(f"\n[INFO] {data[len('MSG:'):]}")
                elif data.startswith("END:"):
                    print("\n" + "="*30)
                    print(data[len("END:"):])
                    print("="*30)
                    break
                else:
                    # Fallback for unexpected data
                    print(data)

        except (KeyboardInterrupt, EOFError):
            print("\nExiting.")
        except ConnectionResetError:
            print("\n[Server disconnected]")
        finally:
            sock.close()

    def start_client(host, port):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            sock.connect((host, port))
            print(f"Connected to Hangman server at {host}:{port}")
            return sock
        except ConnectionRefusedError:
            print(f"Connection failed. Is the server running at {host}:{port}?")
            sys.exit(1)

    # --- Main Execution ---
    def main():
        parser = argparse.ArgumentParser(description="Network Hangman Game")
        group = parser.add_mutually_exclusive_group(required=True)
        group.add_argument("--listen", action="store_true", help="Run as server (hosts the game)")
        group.add_argument("--connect", metavar="HOST", help="Connect to a server at HOST")
        parser.add_argument("--port", type=int, default=5000, help="Port to use (default 5000)")
        
        args = parser.parse_args()

        if args.listen:
            server = Server(args.port)
            server.run()
        elif args.connect:
            sock = start_client(args.connect, args.port)
            run_client_game(sock)

    if __name__ == "__main__":
        try:
            main()
        except (SystemExit, KeyboardInterrupt):
            print("\nShutting down.")
        except Exception as e:
            print(f"An error occurred: {e}")
        finally:
            # The input prompt is removed to allow for non-interactive script termination
            print("Press Enter to exit...")
            sys.stdin.read(1)

except Exception as e:
    print(f"An error occurred during setup: {e}")
    input("Press Enter to exit...")