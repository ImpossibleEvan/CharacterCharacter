try:
    import argparse
    import socket
    import threading
    import sys
    import random

    #!/usr/bin/env python3
    """
    Simple two-way Hangman game for two computers.
    Run one side as server: python hangman.py --listen --port 5000
    Run the other side as client: python hangman.py --connect HOST --port 5000
    The server chooses a word, the client guesses. Use Ctrl+C to exit.
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

    WORDS = [
        "python", "javascript", "programming", "github", "copilot", "developer",
        "socket", "network", "server", "client", "hangman", "terminal"
    ]

    def get_game_state(word, guessed_letters, tries):
        """Constructs the display string for the current game state."""
        display = HANGMAN_PICS[6 - tries]
        
        word_display = ""
        for letter in word:
            if letter in guessed_letters:
                word_display += letter + " "
            else:
                word_display += "_ "
        
        guessed_str = "Guessed letters: " + " ".join(sorted(list(guessed_letters)))
        
        return f"{display}\n\nWord: {word_display}\n{guessed_str}\nTries left: {tries}"

    def run_server_game(conn):
        """Server-side game loop."""
        word = random.choice(WORDS)
        guessed_letters = set()
        tries = 6
        game_over = False

        print(f"Game started. The word is '{word}'.")

        while not game_over:
            # Send current state to client
            state_msg = get_game_state(word, guessed_letters, tries)
            conn.sendall(state_msg.encode())

            # Wait for a guess from the client
            try:
                data = conn.recv(1024)
                if not data:
                    print("\n[Client disconnected]")
                    break
                guess = data.decode().lower().strip()
            except ConnectionResetError:
                print("\n[Client disconnected]")
                break

            # Process the guess
            if len(guess) == 1 and guess.isalpha():
                if guess in guessed_letters:
                    # Letter already guessed, do nothing
                    pass
                elif guess in word:
                    guessed_letters.add(guess)
                else:
                    guessed_letters.add(guess)
                    tries -= 1
            
            # Check for win/loss
            won = all(letter in guessed_letters for letter in word)
            if won:
                final_msg = f"\nCongratulations! You guessed the word: {word}"
                conn.sendall(final_msg.encode())
                game_over = True
            elif tries == 0:
                final_msg = f"\nGame Over! The word was: {word}"
                conn.sendall(final_msg.encode())
                game_over = True
        
        print("Game has ended.")
        conn.close()

    def run_client_game(sock):
        """Client-side game loop."""
        try:
            while True:
                # Receive game state from server
                data = sock.recv(4096)
                if not data:
                    print("\n[Server disconnected]")
                    break
                
                state_msg = data.decode()
                print("\n" + "="*20)
                print(state_msg)

                # Check if game is over
                if "Congratulations" in state_msg or "Game Over" in state_msg:
                    break

                # Get player's guess
                guess = input("Enter your guess (a single letter): ")
                if not guess:
                    guess = " " # Send something to avoid blocking
                
                sock.sendall(guess[0].encode())

        except (KeyboardInterrupt, EOFError):
            print("\nExiting.")
        except ConnectionResetError:
            print("\n[Server disconnected]")
        finally:
            sock.close()

    def start_server(port):
        srv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        srv.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        srv.bind(("0.0.0.0", port))
        srv.listen(1)
        print(f"Hangman server listening on 0.0.0.0:{port} ... waiting for a player.")
        conn, addr = srv.accept()
        print(f"Player connected from {addr[0]}:{addr[1]}")
        srv.close()
        return conn

    def start_client(host, port):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            sock.connect((host, port))
            print(f"Connected to Hangman server at {host}:{port}")
            return sock
        except ConnectionRefusedError:
            print(f"Connection failed. Is the server running at {host}:{port}?")
            sys.exit(1)

    def main():
        parser = argparse.ArgumentParser(description="Network Hangman Game")
        group = parser.add_mutually_exclusive_group()
        group.add_argument("--listen", action="store_true", help="Run as server (hosts the game)")
        group.add_argument("--connect", metavar="HOST", help="Connect to a server at HOST")
        parser.add_argument("--port", type=int, default=5000, help="Port to use (default 5000)")
        
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
            conn = start_server(args.port)
            run_server_game(conn)
        elif args.connect:
            sock = start_client(args.connect, args.port)
            run_client_game(sock)
        else:
            parser.print_help()
            return

    if __name__ == "__main__":
        try:
            main()
        except (SystemExit, KeyboardInterrupt):
            pass
        except Exception as e:
            print(f"An error occurred: {e}")
        finally:
            input("Press Enter to exit...")

except Exception as e:
    print(f"An error occurred during setup: {e}")
finally:
    # This outer finally is for the case where imports fail.
    # The inner finally handles the normal exit.
    pass