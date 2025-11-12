from Isopalia import *


setup("CharacterCharacter")
background(0)
onscreen:pygame.Surface = pygame.Surface((canvas.width, canvas.height))

def draw():
    if mouse.down:
        if mouse.left:
            fill(255)
            noStroke()
            rect(mouse.x-25, mouse.y-25, 50, 50)
        if mouse.right:
            fill(0)
            circle(mouse.x, mouse.y, 100)

def eventHandler(event: pygame.event.Event):
    try:
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                quit()
            textSize(32)
            fill(255)
            text(chr(event.key), mouse.x, mouse.y)
        if event.type == pygame.MOUSEWHEEL:
            pass
    except Exception as e:
        print(e)

try:
    start(draw, nothing, eventHandler)
except Exception as e:
    print(e)
finally:
    input()