from Isopalia import *
import server
import client
import json

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
    global brushSize, drew, chars
    infos = []

    out_msg = json.dumps({
        "x": mouse.x,
        "y": mouse.y,
        "brush": brushSize,
        "drew": drew,
        "chars": chars
    })
    # reset after preparing
    chars = ''
    drew = 0

    if who == 's':
        data = server.checkAll()
        # data is assumed to be dict of client_id -> json-string
        for msg in data.values():
            if msg:
                try:
                    infos.append(json.loads(msg))
                except:
                    pass
        # include server's own message object for clients
        server.sendAll(out_msg)
        infos.append(json.loads(out_msg))
    else:
        data = client.check()
        if data:
            for msg in data.split(';;'):
                if msg:
                    try:
                        infos.append(json.loads(msg))
                    except:
                        pass
        client.send(out_msg)

    # debug overlay unchanged
    switchVisualOutput(frontScreen)
    textSize(12)
    fill(255, 255, 255)
    text(str(len(infos)), 10, 10)
    text(str(out_msg), canvas.width/2, 10)

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
                x, y, bSize, drewReceived = info["x"], info["y"], info["brush"], info["drew"]
                chrs = info["chars"] if "chars" in info else ''
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
                print(e)
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