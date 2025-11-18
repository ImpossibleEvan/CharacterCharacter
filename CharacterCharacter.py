from Isopalia import *
import server
import client
import json
import threading

# Choose to be server or client, and set up networking.
while True:
    who = input("Are you the [s]erver, [c]lient, or [a]lone? /: ").strip().lower()[0]

    if who == 's':
        server.setup()
        break
    elif who == 'c':
        client.setup()
        break
    elif who == 'a':
        print("Running in offline mode.")
        break
    else:
        print("Please enter 's' for server or 'c' for client.")
        continue

setup("CharacterCharacter", 720, 540)
background(0)

backScreen:pygame.Surface = pygame.Surface((canvas.width, canvas.height))
backScreen.fill((0,0,0))
frontScreen:pygame.Surface = pygame.Surface((canvas.width, canvas.height), pygame.SRCALPHA)
frontScreen.fill((0,0,0,0))
ghostScreen:pygame.Surface = pygame.Surface((canvas.width, canvas.height), pygame.SRCALPHA)
ghostScreen.fill((0,0,0,0))

brushSize = 20
brushColor = (255, 255, 255)
savedColors:dict[str, tuple[int, int, int]] = {
    "white": (255, 255, 255),
    "gray": (128, 128, 128),
    "black": (0, 0, 0),
    
    "red": (255, 0, 0),
    "orange": (255, 128, 0),
    "yellow": (255, 255, 0),
    "chart" : (128, 255, 0),
    "green": (0, 255, 0),
    "jade": (0, 255, 128),
    "cyan": (0, 255, 255),
    "sea": (0, 128, 255),
    "blue": (0, 0, 255),
    "purple": (128, 0, 255),
    "magenta": (255, 0, 255),

    "pink": (255, 128, 128),
    "brown": (128, 64, 0),
    "tan": (255, 224, 192),
}
drew:int = 0
chars = ''
hiding = False

def prompt() -> None:
    global brushSize, brushColor, hiding
    while True:
        command = input("/")
        args = command.strip().lower().split()
        if len(args) == 0:
            continue
        match args[0]:
            case "quit" | "exit":
                quit()
            case "size":
                if len(args) >= 2:
                    try:
                        newSize = int(args[1])
                        brushSize = max(1, newSize)
                        print(f"Brush size set to {brushSize}.")
                    except ValueError:
                        print("Invalid brush size. Please enter a number.")
                else:
                    print("Usage: /size <size>")
            case "color":
                if len(args) == 4:
                    try:
                        r = int(args[1])
                        g = int(args[2])
                        b = int(args[3])
                        brushColor = (max(0, min(255, r)), max(0, min(255, g)), max(0, min(255, b)))
                        print(f"Brush color set to {brushColor}.")
                    except ValueError:
                        print("Invalid color values. Please enter three numbers for R G B.")
                elif len(args) == 2 and args[1] == "random":
                    import random
                    brushColor = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
                    print(f"Brush color set to random color {brushColor}.")
                elif len(args) == 2:
                    colorName = args[1]
                    if colorName in savedColors:
                        brushColor = savedColors[colorName]
                        print(f"Brush color set to {brushColor} ({colorName}).")
                    else:
                        print(f"Unknown color name: {colorName}. Available colors: {', '.join(savedColors.keys())}")
                else:
                    print("Usage: /color <R> <G> <B>")
            case "ghost":
                # Create a ghost of whatever is the first argument
                if len(args) >= 2:
                    switchVisualOutput(ghostScreen)
                    textSize(brushSize*2)
                    textAlign("center", "center")
                    fill(*brushColor)
                    text(args[1], canvas.width // 2, canvas.height // 2)
                    
                    # Set all alpha to half transparent
                    arr = pygame.surfarray.pixels_alpha(ghostScreen)
                    arr[:] = (arr[:] // 2)
                    del arr
                else:
                    print("Usage: ghost <character>")
            case "hide":
                hiding = not hiding
                print(f"Information is now {'hidden' if hiding else 'shown'}.")
            case _:
                print(f"Unknown command: {args[0]}")

promptingThread = threading.Thread(target=prompt, daemon=True)
promptingThread.start()

def networkHander() -> tuple:
    global brushSize, brushColor, drew, chars
    
    # If alone, do nothing.
    if who == 'a':
        return tuple()
    
    infos = []

    out_msg = json.dumps({
        "x": mouse.x,
        "y": mouse.y,
        "brush": brushSize,
        "drew": drew,
        "color": str(brushColor),
        "chars": chars
    })
    
    # reset after preparing
    chars = ''
    drew = 0

    if who == 's':
        # If you are the server, it's easy, just check all clients, and send the collection of all of them to each client.

        data = server.checkAll()
        # data is assumed to be dict of client_id -> json-string
        for msg in data.values():
            if msg:
                try:
                    infos.append(json.loads(msg))
                except:
                    pass
        
        for clnt in server.clients.keys(): # For each client's address
            others = list(data.values()) # Get all messages
            if clnt in data:
                others.remove(data[clnt]) # Remove this client's own message to avoid echo
            server.send(';;'.join([out_msg] + others), clnt)
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
    if not hiding:
        switchVisualOutput(frontScreen)
        textSize(12)
        fill(*brushColor)
        text(str(len(infos) + 1), 10, 10)
    return tuple(infos)

def draw():
    global brushSize, brushColor, drew, chars
    switchVisualOutput(backScreen) # Make sure we are editing the background.
    frontScreen.fill((0,0,0,0)) # Make sure the stuff changing each frame is reset.

    # Erase when right-clicking and make a square.
    if mouse.down:
        noStroke()
        if mouse.left:
            fill(*brushColor)
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
                x, y, bSize, drewReceived, bColor = info["x"], info["y"], info["brush"], info["drew"], tuple(map(int, info["color"].strip('()').split(',')))
                chrs = info["chars"] if "chars" in info else ''
                for c in chrs:
                    if c != '':
                        switchVisualOutput(backScreen)
                        textSize(bSize*2)
                        textAlign("center", "center")
                        fill(*bColor)
                        text(c, x, y)

                match drewReceived:
                    case 1:
                        switchVisualOutput(backScreen)
                        noStroke()
                        fill(*bColor)
                        circle(x, y, bSize)
                    case -1:
                        switchVisualOutput(backScreen)
                        noStroke()
                        fill(0)
                        circle(x, y, bSize)
                    case 0:
                        if not hiding:
                            switchVisualOutput(frontScreen)
                            noFill()
                            strokeWeight(1)
                            stroke(0, 255, 255)
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
    canvas.screen.blit(ghostScreen, (mouse.x - canvas.width // 2, mouse.y - canvas.height // 2))

def eventHandler(event: pygame.event.Event):
    global chars, brushSize, brushColor
    switchVisualOutput(backScreen)
    try:
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                quit()
            elif event.key == pygame.K_UP:
                brushColor = (min(255, brushColor[0]+16), min(255, brushColor[1]+16), min(255, brushColor[2]+16))
            elif event.key == pygame.K_DOWN:
                brushColor = (max(0, brushColor[0]-16), max(0, brushColor[1]-16), max(0, brushColor[2]-16))
            elif event.unicode != ';':
                textSize(brushSize*2)
                textAlign("center", "center")
                fill(*brushColor)
                text(event.unicode, mouse.x, mouse.y)
                chars = chars + event.unicode
            else:
                pass
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
    elif who == 'c':
        client.clientSocket.close()
        client.mainThread.join(0.1)