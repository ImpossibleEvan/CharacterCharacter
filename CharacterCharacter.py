from Isopalia import *


setup("CharacterCharacter")
background(0)

backScreen:pygame.Surface = pygame.Surface((canvas.width, canvas.height))
backScreen.fill((0,0,0))
frontScreen:pygame.Surface = pygame.Surface((canvas.width, canvas.height), pygame.SRCALPHA)
frontScreen.fill((0,0,0,0))

brushSize = 20

def draw():
    switchVisualOutput(backScreen) # Make sure we are editing the background.
    frontScreen.fill((0,0,0,0)) # Make sure the stuff changing each frame is reset.

    # Erase when right-clicking and make a square.
    if mouse.down:
        noStroke()
        if mouse.left:
            fill(255)
            circle(mouse.x, mouse.y, brushSize)
        if mouse.right:
            fill(0)
            circle(mouse.x, mouse.y, brushSize)

    # Update brushSize based on mouse scrolling.
    brushSize = max(1, brushSize + mouse.scrolled)

    # Draw a circle the size of the brush to show where it will be draw.
    switchVisualOutput(frontScreen)
    noFill()
    stroke(255)
    strokeWeight(1)
    circle(mouse.x, mouse.y, brushSize)

    # Draw the non-updating background and updating foreground.
    canvas.screen.blit(backScreen)
    canvas.screen.blit(frontScreen)

def eventHandler(event: pygame.event.Event):
    try:
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                quit()
            textSize(canvas.width//20)
            textAlign("center", "center")
            fill(255)
            text(chr(event.key), mouse.x, mouse.y)
    except Exception as e:
        print(e)

try:
    start(draw, nothing, eventHandler)
except Exception as e:
    print(e)
finally:
    input()
