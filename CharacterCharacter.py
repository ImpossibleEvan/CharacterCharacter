from Isopalia import *
import TwoWay

setup("CharacterCharacter", 400, 400)
background(0)

backScreen:pygame.Surface = pygame.Surface((canvas.width, canvas.height))
backScreen.fill((0,0,0))
frontScreen:pygame.Surface = pygame.Surface((canvas.width, canvas.height), pygame.SRCALPHA)
frontScreen.fill((0,0,0,0))

brushSize = 20
drew:int = 0
chars = ''

def draw():
    global brushSize, drew, chars
    switchVisualOutput(backScreen) # Make sure we are editing the background.
    frontScreen.fill((0,0,0,0)) # Make sure the stuff changing each frame is reset.

    # Erase when right-clicking and make a square.
    if mouse.down:
        noStroke()
        if mouse.left:
            fill(255)
            circle(mouse.x, mouse.y, brushSize)
            drew = 1
        if mouse.right:
            fill(0)
            circle(mouse.x, mouse.y, brushSize)
            drew = -1

    # Update brushSize based on mouse scrolling.
    brushSize = max(1, brushSize + mouse.scrolled)

    # Draw a circle the size of the brush to show where it will be draw.
    switchVisualOutput(frontScreen)
    noFill()
    strokeWeight(1)
    stroke(255)
    circle(mouse.x, mouse.y, brushSize)
    stroke(0)
    circle(mouse.x, mouse.y, brushSize-1)

    # Send the current mouse position and brush size to the other client.
    TwoWay.send(f"{mouse.x},{mouse.y},{brushSize},{drew},{chars}")
    # Reset chars and drew after sending.
    chars = ''
    drew = 0

    data = TwoWay.check()
    if data != "":
        try:
            x, y, bSize, drewReceived = map(int, data.split(",")[0:4])
            chrs = data.split(",")[4].split()
            for c in chrs:
                if c != '':
                    switchVisualOutput(backScreen)
                    textSize(bSize*2)
                    textAlign("center", "center")
                    fill(255)
                    text(c, x, y)

            noFill()
            stroke(255, 0, 0)
            circle(x, y, bSize)
            match drewReceived:
                case 1:
                    switchVisualOutput(backScreen)
                    noStroke()
                    fill(255)
                    circle(x, y, bSize)
                case -1:
                    switchVisualOutput(backScreen)
                    noStroke()
                    fill(0)
                    circle(x, y, bSize)

        except Exception as e:
            print(e)

    # Draw the non-updating background and updating foreground.
    canvas.screen.blit(backScreen, (0,0))
    canvas.screen.blit(frontScreen, (0,0))    

def eventHandler(event: pygame.event.Event):
    switchVisualOutput(backScreen)
    try:
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                quit()
            textSize(brushSize*2)
            textAlign("center", "center")
            fill(255)
            text(event.unicode, mouse.x, mouse.y)
            chars = chars + event.unicode
    except Exception as e:
        print(e)

start(draw, nothing, eventHandler)

try:
    pass
except Exception as e:
    print(e)
finally:
    input()
    TwoWay.thread.join()
