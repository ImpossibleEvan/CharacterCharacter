import client
import server
import threading

"""A short fusion script to run either the server or client based on user input."""

who = input("Are you the [s]erver or [c]lient? ").strip().lower()[0]

def run() -> None:
    match who:
        case 's':
            server.main()
        case 'c':
            client.main()

def send(msg: str) -> None:
    match who:
        case 's':
            server.send(msg)
        case 'c':
            client.send(msg)

def check() -> str:
    match who:
        case 's':
            return server.check()
        case 'c':
            return client.check()

def uniqueCheck() -> str:
    match who:
        case 's':
            return server.uniqueCheck()
        case 'c':
            return client.uniqueCheck()

thread = threading.Thread(target=run, daemon=True)
thread.start()