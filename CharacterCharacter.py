from Isopalia import *


setup("CharacterCharacter")

def draw():
    background(0)





def eventHandler(event: pygame.event.Event):
    if event.type == pygame.KEYDOWN:
        text(chr(event.key))
    if event.type == pygame.MOUSEBUTTONDOWN:
        text(f"Mouse button {event.button} pressed at {event.pos}")
        if event.button == 1:
            rect(50, 50, 100, 100, color=Color(255, 0, 0))