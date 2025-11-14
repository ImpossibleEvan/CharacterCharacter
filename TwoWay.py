import client
import server
import threading

"""A short fusion script to run either the server or client based on user input."""

who = input("Are you the [s]erver or [c]lient? ").strip().lower()[0]

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