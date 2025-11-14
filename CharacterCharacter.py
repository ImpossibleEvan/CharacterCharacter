from Isopalia import *
import server
import client

# Choose to be server or client, and set up networking.
while True:
    who = input("Are you the [s]erver or [c]lient? /: ").strip().lower()[0]

    if who == 's':
        server.setup()
        break
    elif who == 'c':
        client.setup()
        break
    else:
        print("Please enter 's' for server or 'c' for client.")
        continue

setup("CharacterCharacter", 400, 400)
background(0)

backScreen:pygame.Surface = pygame.Surface((canvas.width, canvas.height))
backScreen.fill((0,0,0))
frontScreen:pygame.Surface = pygame.Surface((canvas.width, canvas.height), pygame.SRCALPHA)
frontScreen.fill((0,0,0,0))

brushSize = 20
drew:int = 0
chars = ''

def networkHander() -> tuple:
    # Clients send their data in the form of "x;y;brushSize;drew;chars"
    # Servers receive from all clients and send back all data of every player in a longer string seperated double ';' (';;')
    # Clients receive this long string and parse it.
    # Return a tuple of all received infos, each just the data string originating from one client.

    infos = []

    # If you are the server
    if who == 's':
        # Get all data from all clients
        data = server.checkAll()

        # Add all client data to a list
        for msg in data.values():
            infos.append(msg)

        # Add own data
        infos.append(f"{mouse.x};{mouse.y};{brushSize};{drew};`{chars}")

        outSignal = ';;'.join(infos)

        # Send everything to the clients
        server.sendAll(outSignal)
    else:
        data = client.check()

        # Parse the long string into individual messages
        for msg in data.split(';;'):
            infos.append(msg)

        outSignal = f"{mouse.x};{mouse.y};{brushSize};{drew};`{chars}"

        client.send(outSignal)

    switchVisualOutput(frontScreen)
    textSize(12)
    fill(255, 255, 255)
    text(str(len(infos)), 10, 10)
    text(str(outSignal), canvas.width/2, 10)
    return tuple(infos)

def draw():
    global brushSize, drew, chars
    switchVisualOutput(backScreen) # Make sure we are editing the background.
    frontScreen.fill((0,0,0,0)) # Make sure the stuff changing each frame is reset.

    # Erase when right-clicking and make a square.
    if mouse.down:
        noStroke()
        if mouse.left:
            fill(255, 255, 255)
            circle(mouse.x, mouse.y, brushSize)
            drew = 1
        if mouse.right:
            fill(0, 0, 0)
            circle(mouse.x, mouse.y, brushSize)
            drew = -1

    # Handle networking.
    infos:list[str] = networkHander()    

    # Process all received infos.
    for info in infos:
        if info != "":
            try:
                x, y, bSize, drewReceived = map(int, info.split(";")[0:4])
                chrs = ''.join(list(info.split(";")[4]))[1:] if len(info.split(";")) > 4 else ''
                for c in chrs:
                    if c != '':
                        switchVisualOutput(backScreen)
                        textSize(bSize*2)
                        textAlign("center", "center")
                        fill(255, 255, 255)
                        text(c, x, y)

                switchVisualOutput(frontScreen)
                noFill()
                stroke(255, 0, 0)
                circle(x, y, bSize)
                match drewReceived:
                    case 1:
                        switchVisualOutput(backScreen)
                        noStroke()
                        fill(255, 255, 255)
                        circle(x, y, bSize)
                    case -1:
                        switchVisualOutput(backScreen)
                        noStroke()
                        fill(0)
                        circle(x, y, bSize)
                
                # Reset after processing
                chars = ''
                drew = 0

            except Exception as e:
                print(infos)
    else:
        pass

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
    # ^^^ This was done last to make sure it's on top of everything.

    # Draw the non-updating background and updating foreground.
    canvas.screen.blit(backScreen, (0,0))
    canvas.screen.blit(frontScreen, (0,0))    

def eventHandler(event: pygame.event.Event):
    global chars
    switchVisualOutput(backScreen)
    try:
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                quit()
            if event.unicode != ';':
                textSize(brushSize*2)
                textAlign("center", "center")
                fill(255)
                text(event.unicode, mouse.x, mouse.y)
                chars = chars + event.unicode
            else:
                pass
                # startprompt()
    except Exception as e:
        print(e)

start(draw, nothing, eventHandler)

try:
    pass
except Exception as e:
    print(e)
finally:
    input()

    # Clean up networking threads and sockets
    if who == 's':
        server.serverSocket.close()
        server.listenThread.join(0.1)
        server.sendingThread.join(0.1)
        server.welcomeThread.join(0.1)
    else:
        client.clientSocket.close()
        client.mainThread.join(0.1)