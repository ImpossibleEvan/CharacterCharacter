from __future__ import annotations
from typing import Final
import time
import random as r
from typing import Union, Literal
from Morfi import *
from Pycessing import *

"""
Isopalia meaning "drawing" in Greek. This is a PyGame library that is based on ProcessingJS and Unity all at once in Python.
Documentation:
The main loop runs each frame, and you define this and plug it into Isopalia.start().
There are three states the main loop can be in:
1. "unpaused"
2. "paused"
3. "prompting"
The only difference between "unpaused" and "paused" is that they can be swapped between with the pause() and unpause() functions, and unpaused is the default.
"prompting" is used for when you want to show a prompt to the user, such as a text input or a confirmation dialog.
You can start a prompt with the prompt() function, which takes in text that is shown to the user (like a question) and the name of the channel to store the response in.
prompt() does NOT return the response, it just starts the prompt.
The answer is stored in the channel, and you can access the response with the getPromptOutput() function, with the option to clear the channel after accessing it, much like events.

Isopalia is rather small, because it ties together two larger libraries, Pycessing and Morfi.
Pycessing is a Python port of ProcessingJS, which is a JavaScript library for creative coding. Unfortunately, it does not support opacity of shapes since Pygame does not support it.
Morfi has complex shape data structures, such as Point, Line, Rect, and a lot more that can all be compared for collision and other stuff.
Morfi supports faster initialization of complex shapes, using the direct constructor, such as Rect(Point(0, 0), Size(100, 100)) or R(0, 0, 100, 100) for flexible initialization.

"""

class IsopaliaException(Exception): pass
class DrawingError(IsopaliaException): pass

def _returnFalse(*args, **kwargs) -> Literal[False]:
    """Returns False. Used as a default function for SmartButton."""
    return False

def _returnTrue(*args, **kwargs) -> Literal[True]:
    """Returns True. Used as a default function for SmartButton."""
    return True

def nothing(*args, **kwargs) -> None:
    """The None of functions. Does nothing."""
    pass

def seedrand(min, max, seed):
    """Generates a uniform random number between min and max using a seed."""
    foo = max - min

    a = 1103515245
    b = 12345
    c = 2 ** 31

    seed = (a * seed + b) % c
    seed = (a * seed + b) % c
    seed = (a * seed + b) % c

    bar = seed / c * foo
    bar += min
    return bar


def step(value:float, target:float, step:float) -> float:
    """Steps the value towards the target by the given step size. Returns the new value."""
    if value < target:
        return min(value + step, target)
    elif value > target:
        return max(value - step, target)
    else:
        return value

def chancePerSecond(chance:float) -> bool:
    """Returns True with a chance of chance per second."""
    if r.random() < chance * dt(1):
        return True
    return False

# Advanced data structures specifically engineered for game development.

class WeightedSet:
    def __init__(self, dictOfStuff:dict):
        self.elements = list(dictOfStuff.keys())
        self.weights = list(dictOfStuff.values())
        self.totalWeight = sum(self.weights)

    def random(self) -> str | None:
        """Returns a random element from the set, weighted by their weights."""
        if self.totalWeight == 0:
            return None

        rand = r.random() * self.totalWeight
        for i, weight in enumerate(self.weights):
            rand -= weight
            if rand < 0:
                return self.elements[i]
        return None

    def add(self, element:str, weight:float):
        """Adds an element with a specified weight to the set."""
        self.elements.append(element)
        self.weights.append(weight)
        self.totalWeight += weight

    def remove(self, element:str):
        """Removes an element from the set."""
        if element in self.elements:
            index = self.elements.index(element)
            self.elements.pop(index)
            self.weights.pop(index)
            self.totalWeight -= self.weights[index]

    def clear(self):
        """Clears the set."""
        self.elements.clear()
        self.weights.clear()
        self.totalWeight = 0.0

class GridNode:
    """A node for a grid-based structure. A more expandable version of storing values in a 2D Matrix, by eliminating the need for empty spaces."""
    directionToID:dict[str,int] = {
        "up" : 0,
        "right" : 1,
        "down" : 2,
        "left" : 3,
    }
    IDToDirection:list[str] = ["up", "right", "down", "left"]
    
    def __init__(self, origin:GridNode = None, direction:int = None, value:object = None):
        """Creates a new GridNode. If origin and direction are provided, it will create a new node in the specified direction from the origin node."""
        self.doors:list[GridNode] = [None, None, None, None]
        self.stitches:list[bool] = [False, False, False, False]
        self.original:GridNode = None
        self.value:GridNodeInterior = value

        if origin != None and direction != None:
            newx = origin.x + (direction == 1) - (direction == 3)
            newy = origin.y + (direction == 0) - (direction == 2)
            check = origin.search(newx, newy)

            if check == None:
                self.doors[(direction-2)%4] = origin
                self.createdFrom:int = (direction-2)%4
                self.x = newx
                self.y = newy
                origin.doors[direction%4] = self
            else:
                self.original = check
                origin.stitches[direction%4] = True
                origin.doors[direction%4] = check
                check.doors[(direction+2)%4] = origin
                check.stitches[(direction+2)%4] = True
        else:
            self.createdFrom:int = None
            self.x:int = 0
            self.y:int = 0
    
    def parent(self) -> GridNode:
        if self.createdFrom != None:
            return self.doors[self.createdFrom]
        else:
            return None

    def _search(self, x, y) -> GridNode:
        result = None
        if self.x == x and self.y == y:
            return self
            
        for i in range(4):
            if (self.doors[i] != None) and (not self.stitches[i]):
                if i != self.createdFrom:
                    temp = self.doors[i]._search(x, y)
                    if temp != None:
                        result = temp
                
        return result
                
    def search(self, x, y):
        return self.rootNode()._search(x, y)

    def rootNode(self) -> GridNode:
        curr:GridNode = self
        while curr.parent() != None:
            curr = curr.parent()
        return curr

    def coords(self) -> tuple:
        return (self.x, self.y)

    def branch(self, direction:int, safe=True) -> GridNode:
        if self.doors[direction] == None:
            newnode:GridNode = GridNode(self, direction)
            if newnode.original != None:
                return newnode.original
            else:
                return newnode
        else:
            if safe:
                return self.doors[direction]
            else:
                raise Exception("GridNodeOverlapException")
    
    def linkedRooms(self) -> list[GridNode]:
        """Return a list of linked rooms."""
        ret:list[GridNode] = []
        for i in range(4):
            if self.doors[i] != None:
                ret.append(self.doors[i])
        return ret

    def uniqueChildren(self) -> list[GridNode]:
        ret:list[GridNode] = []
        for i in range(4):
            if (self.doors[i] != None) and (not self.stitches[i]) and (i != self.createdFrom):
                ret.append(self.doors[i])
        return ret
    
    def descendants(self) -> list[GridNode]:
        ret = [self]
        for child in self.uniqueChildren():
            for d in child.descendants():
                ret.append(d)
        return ret
    
    def random(self) -> GridNode:
        return r.choice(self.rootNode().descendants())

    def hasDoor(self, direction:int|str) -> bool:
        """Check if the node has a door in the specified direction."""
        if direction in range(0,4):
            return self.doors[direction] != None
        elif direction in GridNode.directionToID.keys():
            return self.doors[GridNode.directionToID[direction]] != None
        else:
            raise Exception("Invalid GridNode.hasDoor(direction) input, please use up, right, down, left, or numbers 0-3")

    def get(self, direction:str|int) -> GridNode:
        try:
            if type(direction) == str:
                direction = GridNode.directionToID[direction]
            elif direction in range(0,4):
                return self.doors[direction]
            else:
                raise Exception("Invalid GridNode.get(direction) input, please use up, right, down, left, or numbers 0-3")
        except:
            raise Exception("Failed to GridNode.get(direction) input, please use up, right, down, left, or numbers 0-3")
    
    def distanceTo(self, other:GridNode) -> int:
        """Returns the Manhattan distance to another GridNode."""
        return abs(self.x - other.x) + abs(self.y - other.y)
    
    def farthestFrom(self) -> GridNode:
        """Returns the farthest node from this node."""
        return max(self.rootNode().descendants(), key = lambda n: self.distanceTo(n))

    def __str__(self):
        return "+---" + ["--","  "][self.doors[0] != None] + "---+" + "\n|        |\n" + ["|"," "][self.doors[3] != None] + "   []   " + ["|"," "][self.doors[1] != None] + "\n|        |\n" + "+---" + ["--","  "][self.doors[2] != None] + "---+"

class GridNetwork:
    """
    A network of GridNodes. It is a tree-like structure that can be used to represent a grid-based structure.
    Has many useful functions to get nodes in the network.
    The root node is the starting point of the network, and all other nodes are descendants of the root node.
    """
    def __init__(self):
        self.root = GridNode()
    def all(self) -> list[GridNode]:
        """Return all nodes in the network."""
        return self.root.descendants()
    def allConnections(self) -> list[tuple[GridNode, GridNode]]:
        """Return all connections in the network as tuples of (node1, node2)."""
        connections = []
        for node in self.root.descendants():
            for i in range(4):
                if node.doors[i] != None and not node.stitches[i]:
                    connections.append((node, node.doors[i]))
        return connections
    def allConnectionsCoords(self) -> list[tuple[tuple[int, int], tuple[int, int]]]:
        """Return all connections in the network as tuples of ((x1, y1), (x2, y2))."""
        connections = []
        for node in self.root.descendants():
            for i in range(4):
                if node.doors[i] != None and not node.stitches[i]:
                    connections.append((node.coords(), node.doors[i].coords()))
        return connections
    def __list__(self) -> list[GridNode]:
        return self.root.descendants()
    def __getitem__(self, index:int) -> GridNode:
        return self.root.descendants()[index]
    def __len__(self) -> int:
        return len(self.root.descendants())
    def random(self, excludeRoot:bool=False) -> GridNode:
        choice = r.choice(self.root.descendants())
        if excludeRoot and choice == self.root:
            return self.random(excludeRoot)
        return choice
    def topMost(self) -> GridNode:
        """Return the node with the highest Y position."""
        return max(self.root.descendants(), key = lambda node: node.y)
    def bottomMost(self) -> GridNode:
        """Return the node with the lowest Y position."""
        return min(self.root.descendants(), key = lambda node: node.y)
    def leftMost(self) -> GridNode:
        """Return the node with the lowest X position."""
        return min(self.root.descendants(), key = lambda node: node.x)
    def rightMost(self) -> GridNode:
        """Return the node with the highest X position."""
        return max(self.root.descendants(), key = lambda node: node.x)

class GridNodeInterior:
    """An empty class to be overridden by the user. It is used to represent a room in a grid network."""

class AttributeToString:
    """Using dot notation to get an attribute returns the string of the attribute name."""
    def __getattribute__(self, name):
        return name

new:AttributeToString = AttributeToString()
s:AttributeToString = AttributeToString()

class Sack:
    """
    A sack stores a set of strings that can be accessed with dot notation.
    If it is in the sack, returns true, if not return false.
    Can also be manipulated through other methods.
    Should be used to store attributes of a thing that can either exist or not.
    It's flexible so a dictionary containing every possible attribute is not needed. (Dot notation can be used for convenience.)
    In other words, it is a flexible collect of .is___ variables.
    """
    def __init__(self, *args):
        self._sack = set(args)
    
    def __contains__(self, item:str) -> bool:
        return item in self._sack
    
    def __iter__(self):
        return iter(self._sack)
    
    def add(self, item:str) -> None:
        """Adds an item to the sack."""
        self._sack.add(item)
    
    def remove(self, item:str) -> None:
        """Removes an item from the sack."""
        self._sack.remove(item)
    
    def clear(self) -> None:
        """Clears the sack."""
        self._sack.clear()
    
    # Attribute access methods

    def __getattribute__(self, name:str) -> bool | object:
        if name.startswith('_'):
            return super().__getattribute__(name)
        if name in self._sack:
            return True
        else:
            return False
        
    def __setattr__(self, name, value):
        if name.startswith('_'):
            super().__setattr__(name, value)
        else:
            if value:
                self._sack.add(name)
            else:
                self._sack.discard(name)
    
    def __delattr__(self, name):
        if name.startswith('_'):
            super().__delattr__(name)
        else:
            self._sack.discard(name)

    # Item access methods

    def __getitem__(self, item:str) -> bool:
        """Returns True if the item is in the sack, False otherwise."""
        return item in self._sack
    
    def __setitem__(self, item:str, value:bool) -> None:
        """Sets the item in the sack to True if value is True, otherwise removes it."""
        if value:
            self._sack.add(item)
        else:
            self._sack.discard(item)
    
    def __delitem__(self, item:str) -> None:
        """Removes the item from the sack."""
        self._sack.discard(item)

    def __len__(self) -> int:
        """Returns the number of items in the sack."""
        return len(self._sack)
    
    def __bool__(self) -> bool:
        """Returns True if the sack is not empty, False otherwise."""
        return len(self._sack) > 0
    
    def __repr__(self) -> str:
        """Returns a string representation of the sack."""
        return "Sack(" + ", ".join(self._sack) + ")"

    def __str__(self):
        return "Sack(" + ", ".join(self._sack) + ")"
    
    def __eq__(self, other) -> bool:
        """Checks if two sacks are equal."""
        if isinstance(other, Sack):
            return self._sack == other._sack
        return False
    
    def __ne__(self, other) -> bool:
        """Checks if two sacks are not equal."""
        if isinstance(other, Sack):
            return self._sack != other._sack
        return True
    
    def __hash__(self) -> int:
        """Returns a hash of the sack."""
        return hash(frozenset(self._sack))

# Style related classes

class Color:
    __slots__ = ('r', 'g', 'b')
    def __init__(self, r:int = None, g:int = None, b:int = None):
        self.set(r, g, b)
    def set(self, r:int, g:int, b:int) -> None:
        """Sets the color values."""
        if g == None and b == None:
            g = r
            b = r
        elif b == None:
            b = 0

        self.r:int = r
        self.g:int = g
        self.b:int = b
    def __str__(self):
        return f"Color({self.r}, {self.g}, {self.b})"
    def __repr__(self):
        return self.__str__()
    def __add__(self, other):
        if not isinstance(other, Color):
            return NotImplemented
        return Color(min(max(self.r + other.r, 0), 255), min(max(self.g + other.g, 0), 255), min(max(self.b + other.b, 0), 255))
    def __sub__(self, other):
        if not isinstance(other, Color):
            return NotImplemented
        return Color(min(max(self.r - other.r, 0), 255), min(max(self.g - other.g, 0), 255), min(max(self.b - other.b, 0), 255))
    def lerp(self, other:Color|tuple, t:float) -> Color:
        """Linearly interpolates between two colors."""
        if isinstance(other, tuple):
            other = Color(*other)
        if not isinstance(other, Color):
            raise TypeError("other must be a Color")
        return Color(int(self.r + (other.r - self.r) * t), int(self.g + (other.g - self.g) * t), int(self.b + (other.b - self.b) * t))
    def __eq__(self, other):
        if not isinstance(other, Color):
            return False
        return (self.r == other.r and self.g == other.g and self.b == other.b)
    def __ne__(self, other):
        return not self.__eq__(other)
    def __lt__(self, other):
        if not isinstance(other, Color):
            return NotImplemented
        return (self.r + self.g + self.b) < (other.r + other.g + other.b)
    def __le__(self, other):
        if not isinstance(other, Color):
            return NotImplemented
        return (self.r + self.g + self.b) <= (other.r + other.g + other.b)
    def __gt__(self, other):
        if not isinstance(other, Color):
            return NotImplemented
        return (self.r + self.g + self.b) > (other.r + other.g + other.b)
    def __ge__(self, other):
        if not isinstance(other, Color):
            return NotImplemented
        return (self.r + self.g + self.b) >= (other.r + other.g + other.b)
    def __hash__(self):
        return hash((self.r, self.g, self.b))
    def __int__(self):
        return (self.r << 16) + (self.g << 8) + self.b
    def __float__(self):
        return (self.r + self.g + self.b) / 3.0
    def __bool__(self):
        return (self.r != 0 or self.g != 0 or self.b != 0)
    def __getitem__(self, key:int):
        if key == 0:
            return self.r
        elif key == 1:
            return self.g
        elif key == 2:
            return self.b
        else:
            raise IndexError("Index out of range.")
    def __setitem__(self, key:int, value:int):
        if key == 0:
            self.r = value
        elif key == 1:
            self.g = value
        elif key == 2:
            self.b = value
        else:
            raise IndexError("Index out of range.")
    def __iter__(self):
        yield self.r
        yield self.g
        yield self.b
    def clone(self) -> Color:
        """Returns a copy of the color."""
        return Color(self.r, self.g, self.b)
    def alteredClone(self, delta:float) -> Color:
        """Returns a copy of the color with each channel altered by a value from -delta to delta."""
        return Color(
            int(min(max(self.r + r.uniform(-delta, delta), 0), 255)),
            int(min(max(self.g + r.uniform(-delta, delta), 0), 255)),
            int(min(max(self.b + r.uniform(-delta, delta), 0), 255))
        )
    
    @staticmethod
    def fromHex(hex_str:str) -> Color:
        """Creates a Color object from a hex string."""
        if hex_str.startswith("#"):
            hex_str = hex_str[1:]
        if len(hex_str) != 6:
            raise ValueError("Hex string must be 6 characters long.")
        r = int(hex_str[0:2], 16)
        g = int(hex_str[2:4], 16)
        b = int(hex_str[4:6], 16)
        return Color(r, g, b)
    
    @staticmethod
    def fromRGB(red:int, green:int, blue:int) -> Color:
        """Creates a Color object from RGB values."""
        return Color(red, green, blue)
    
    @staticmethod
    def fromHSL(hue:int, saturation:int, lightness:int) -> Color:
        """Creates a Color object from HSL values."""
        c = (1 - abs(2 * lightness / 100 - 1)) * saturation / 100
        x = c * (1 - abs((hue / 60) % 2 - 1))
        m = lightness / 100 - c / 2
        if hue < 60:
            r, g, b = c, x, 0
        elif hue < 120:
            r, g, b = x, c, 0
        elif hue < 180:
            r, g, b = 0, c, x
        elif hue < 240:
            r, g, b = 0, x, c
        elif hue < 300:
            r, g, b = x, 0, c
        else:
            r, g, b = c, 0, x
        return Color(int((r + m) * 255), int((g + m) * 255), int((b + m) * 255))
    
    @staticmethod
    def random() -> Color:
        """Generates a random color."""
        return Color(r.randint(0, 255), r.randint(0, 255), r.randint(0, 255))

class Style:
    __slots__ = ('fill', 'stroke', 'weight', 'edge')
    def __init__(self, fill:Color = None, stroke:Color = None, weight:int = None, edge = 0):
        self.fill:Color = fill if fill is not None else Color(200, 200, 200)
        self.stroke:Color = stroke if stroke is not None else Color(0, 0, 0)
        self.weight:int = weight if weight is not None else 1
        self.edge:int = edge if edge is not None else 0
    def __str__(self):
        return f"Style(fill={self.fill}, stroke={self.stroke}, weight={self.weight}, edge={self.edge})"
    def __repr__(self):
        return self.__str__()
    def __eq__(self, other):
        if not isinstance(other, Style):
            return False
        return (self.fill == other.fill and self.stroke == other.stroke and self.weight == other.weight and self.edge == other.edge)
    def __ne__(self, other):
        return not self.__eq__(other)
    def apply(self):
        """Applies the style to the canvas. And returns a reconstruction of the old style object."""
        old_style = Style()
        if self.fill is not None:
            old_style.fill = Color(*fill(*self.fill))
        if self.stroke is not None:
            old_style.stroke =  Color(*stroke(*self.stroke))
        if self.weight is not None:
            strokeWeight(self.weight)
    def clone(self):
        return Style(self.fill, self.stroke, self.weight, self.edge)
    @staticmethod
    def default():
        return Style(Color(200, 200, 200), Color(0, 0, 0), 1, 0)

# Complex shapes and objects

class Text:
    __slots__ = ('txt', 'size', 'color', 'font', 'alignment', 'text')
    def __init__(self, txt:str, size:int = 12, color:Color = Color(0, 0, 0), font:str = 'C:/Windows/Fonts/calibri.ttf', alignment:tuple[str, str] = ("LEFT", "TOP")):
        self.text:str = txt
        self.size:int = size
        self.color:Color = color
        self.font:str = font
        self.alignment:tuple[str, str] = alignment

    def draw(self, x, y):
        textSize(self.size)
        createFont(self.font, self.size)
        fill(*self.color)
        textAlign(*self.alignment)
        text(self.text, x, y)

class Sound:
    __slots__ = ('sound', 'volume')
    cache:dict[str, pygame.mixer.Sound] = {}
    def __init__(self, sound:str, volume:float = 1.0):
        if sound not in Sound.cache:
            Sound.cache[sound] = load_sound(sound)
        self.sound:pygame.mixer.Sound = Sound.cache[sound]
        self.volume:float = volume

    def play(self):
        self.sound.set_volume(self.volume)
        self.sound.play()

class SoundSet:
    # A class to manage a set of sounds.
    __slots__ = ('sounds',)
    def __init__(self, sounds:list[Sound] = None):
        self.sounds:list[Sound] = sounds if sounds is not None else []
    def play(self):
        self.sounds[r.randint(0, len(self.sounds) - 1)].play() if self.sounds else None

class Image:
    __slots__ = ('img', 'rect')
    cache = {}
    def __init__(self, img:str, *args):
        self.img:pygame.surface.Surface = load_image(img) if img not in Image.cache else Image.cache[img]
        if img not in Image.cache:
            Image.cache[img] = self.img
        self.rect:Rect = R(*args) if len(args) != 0 else Rect(Point(0, 0), Size(self.img.get_width(), self.img.get_height()))

    def draw(self, angle:float = 0, flipX:bool = False, flipY:bool = False):
        if self.rect is None:
            raise DrawingError("Image has no defined Rect. Use drawAt() to draw the image at a specific position without a Rect().")
        image(self.img, self.rect.pos.x, self.rect.pos.y, self.rect.size.width, self.rect.size.height, angle=angle, flipX=flipX, flipY=flipY)

    def drawAt(self, x:int, y:int, w:int = None, h:int = None):
        """Draws the image at the specified position with the specified width and height."""
        if self.rect is None and (w is None or h is None):
            raise DrawingError("Image has no defined Rect. Use draw() to draw the image with a Rect().")
        if w is None:
            w = self.rect.size.width
        if h is None:
            h = self.rect.size.height
        image(self.img, x, y, w, h)
    
    def transform(self, *args):
        self.rect.become(R(*args))

class Sprite:
    __slots__ = ('img',)
    cache = {}
    def __init__(self, img:str):
        if img not in Sprite.cache:
            Sprite.cache[img] = load_image(img)
        self.img:pygame.surface.Surface = Sprite.cache[img]

    def drawAt(self, x:int, y:int, w:int, h:int, angle:float = 0):
        """Draws the image at the specified position with the specified width and height."""
        image(pygame.transform.rotate(self.img, angle), x, y, w, h)

class Animation:
    """A class to handle animations. It can be used to animate a sprite or an image."""

    @staticmethod
    def stepBehavior(anim:Animation):
        anim.frameIndex = constrain(anim.frameIndex + 1, 0, len(anim.data[anim.mode]) - 1)
    
    @staticmethod
    def loopBehavior(anim:Animation):
        anim.frameIndex = (anim.frameIndex + 1) % len(anim.data[anim.mode])
    
    @staticmethod
    def backCycleBehavior(anim:Animation):
        """When reaching the end, it moves back by (anim.special) frames, then continues forward."""
        if anim.frameIndex + anim.special >= len(anim.data[anim.mode]):
            anim.frameIndex = max(0, anim.frameIndex - anim.special)
        else:
            anim.frameIndex += 1
        if anim.frameIndex >= len(anim.data[anim.mode]):
            anim.frameIndex = 0
    
    @staticmethod
    def bounceBehavior(anim:Animation):
        """Bounces back and forth between the first and last frames."""
        if anim.frameIndex == 0:
            anim.special = 1
        elif anim.frameIndex == len(anim.data[anim.mode]) - 1:
            anim.special = -1
        anim.frameIndex += anim.special
        if anim.frameIndex < 0 or anim.frameIndex >= len(anim.data[anim.mode]):
            anim.special *= -1
            anim.frameIndex += anim.special

    def __init__(self, frames:dict[str, list[Sprite]], framerate:float = 30, behavior:function = nothing, special:int = 0):
        """Creates a new animation with the given frames and frame rate."""
        self.data:dict[str, list[Sprite]] = frames
        self.framerate:float = framerate
        self.frameIndex:int = 0
        self.behavior:function = behavior
        self.mode = "start"
        self.special = special  # Special is used to do other stuff with behaviors.

    def current(self) -> Image:
        """Returns the current frame of the animation."""
        return self.data[self.mode][self.frameIndex] if self.mode in self.data else None

class Sound:
    """A class to handle sounds. It can be used to play a sound effect or music."""
    def __init__(self, sound:str):
        """Creates a new sound with the given file path."""
        self.sound:pygame.mixer.Sound = load_sound(sound)
    
    def play(self, loops:int = 0, maxtime:int = 0, fade_ms:int = 0):
        """Plays the sound with the given parameters."""
        self.sound.play(loops, maxtime, fade_ms)
    
    def stop(self):
        """Stops the sound."""
        self.sound.stop()
    
    def setVolume(self, volume:float):
        """Sets the volume of the sound."""
        self.sound.set_volume(volume)
    
    def getVolume(self) -> float:
        """Returns the volume of the sound."""
        return self.sound.get_volume()

class Button:
    __slots__ = ('rect', 'style', 'text', 'corner_rounding', 'child')
    defaultStyle = Style(Color(255, 255, 255), Color(0, 0, 0), 1, 0)
    defaultText = Text("Button", 12, Color(0, 0, 0), 'C:/Windows/Fonts/calibri.ttf')
    def __init__(self, rect:Rect, text:Text, styleOrImage:Style|Image = None, textAlignment:tuple[str, str] = ("CENTER", "CENTER"), cnr=0, child:object = None):
        """Creates a new button with the given rectangle, text, style or image, corner rounding, and an optional child object. Styles and Texts will default if not provided."""
        self.rect:Rect = rect
        self.style:Style|Image = styleOrImage if styleOrImage is not None else Button.defaultStyle
        self.text:Text = text if text is not None else (Text(text) if isinstance(text, str) else Button.defaultText)
        self.text.alignment = textAlignment  # Set the text alignment to the given value.
        self.child:object = child  # This can be used to store a value associated with the button.

        self.corner_rounding = cnr
    
    def setText(self, newText):
        self.text.text = newText

    def draw(self):
        if isinstance(self.style, Style):
            self.style.apply()
            rect(self.rect.pos.x, self.rect.pos.y, self.rect.size.width, self.rect.size.height, self.corner_rounding)
        elif isinstance(self.style, Image):
            self.style.drawAt(*self.rect.pos.x, *self.rect.size)
        self.text.draw(self.rect.pos.x + self.rect.size.width/2, self.rect.pos.y + self.rect.size.height/2)
    
    def mouseOver(self):
        return mouse.x > self.rect.pos.x and mouse.y > self.rect.pos.y and mouse.y < self.rect.pos.y + self.rect.size.height and mouse.x < self.rect.pos.x + self.rect.size.width
    
    def isPressed(self,mouseButton="left"):
        if self.mouseOver():
            if mouseButton == "left":
                return mouse.left
            elif mouseButton == "center":
                return mouse.middle
            elif mouseButton == "right":
                return mouse.right
        return False
    
    def isClicked(self,mouseButton="left"):
        if self.mouseOver():
            if mouseButton == "left":
                return mouseClicked(1)
            elif mouseButton == "center":
                return mouseClicked(2)
            elif mouseButton == "right":
                return mouseClicked(3)
        return False
    
    def isReleased(self,mouseButton="left"):
        if self.mouseOver():
            if mouseButton == "left":
                return (pmouse.left is True and mouse.left is False)
            elif mouseButton == "center":
                return (pmouse.middle is True and mouse.middle is False)
            elif mouseButton == "right":
                return (pmouse.right is True and mouse.right is False)
        return False

class IButton:
    all:list[IButton] = []
    def __init__(self, button:Button, shouldDraw:function = None, shouldCheck:function = None, onHover:function = None, onNotHover:function = None, onClick:function = None, onRelease:function = None, name:str = None):
        """A smart button that can have custom functions for drawing, hovering, clicking, and releasing.
        :param button: The button to use.
        :param shouldDraw: A function that returns True if the button should be drawn, False otherwise.
        :param shouldCheck: A function that returns True if the button should be checked for hover, click, and release, False otherwise.
        :param onHover: A function that is called when the button is hovered over.
        :param onClick: A function that is called when the button is clicked.
        :param onRelease: A function that is called when the button is released.
        If shouldDraw and shouldCheck are not provided, the button will always be drawn and checked. If one is provided, the other will be used in its place.
        """
        self.button:Final[Button] = button
        self.shouldDraw:function = shouldDraw if shouldDraw is not None else (shouldCheck if shouldCheck is not None else _returnTrue)
        self.shouldCheck:function = shouldCheck if shouldCheck is not None else (shouldDraw if shouldDraw is not None else _returnTrue)
        self.onHover:function = onHover if onHover is not None else IButton._defaultHover
        self.onNotHover:function = onNotHover if onNotHover is not None else IButton._defaultNotHover
        self.onClick:function = onClick if onClick is not None else nothing
        self.onRelease:function = onRelease if onRelease is not None else nothing
        print(f"Created IButton: {name}") if name is not None else print("Created IButton")
        IButton.all.append(self)

    def tick(self):
        """Checks if the button should be drawn and if it should be checked for hover, click, and release."""
        if self.shouldDraw(self.button):
            self.button.draw()
        if self.shouldCheck(self.button):
            if self.button.mouseOver():
                if self.onHover is not None:
                    self.onHover(self.button)
                if self.button.isClicked():
                    if self.onClick is not None:
                        self.onClick(self.button)
            else:
                if self.onNotHover is not None:
                    self.onNotHover(self.button)
            if self.button.isReleased():
                if self.onRelease is not None:
                    self.onRelease(self.button)
    
    @staticmethod
    def _defaultHover(button:Button):
        """Default hover function that changes the stroke color to white."""
        button.style.stroke.set(255, 255, 255)
    
    @staticmethod
    def _defaultNotHover(button:Button):
        """Default not hover function that changes the stroke color to black."""
        button.style.stroke.set(0, 0, 0)

class Unique:
    """A class that returns an empty object used for special values."""
    def __init__(self):
        self.id = id(self)
    def __str__(self):
        return f"Unique({self.id})"

Drawable = Union[Point, Line, Ray, Rect, Ellipse, Circle, Triangle, Sprite, Image, Text, Button, Style, None]
ColorType = Union[Color, tuple[int, int, int]]
transparent = Unique()

def draw(element:Drawable, _fill:ColorType = None, _stroke:ColorType = None, _weight:int = None, edge = 0, style:Style = None, location:Point = None, scale:Size = None, angle:float = 0) -> None:
    """
    Draws a shape on the canvas.
    Location and scale only do something if the element is an Image or Text.
    """
    oldFill:ColorType = None
    oldStroke:ColorType = None
    oldWeight:int = None

    if style is not None:
        style.use()

    if _fill is transparent:
        noFill()
    elif _fill is not None:
        oldFill = fill(*_fill)

    if _weight == 0 or _stroke is transparent:
        noStroke()
    elif _stroke is not None:
        oldStroke = stroke(*_stroke)

    if _weight is not None:
        oldWeight = strokeWeight(_weight)

    if isinstance(element, Point):
        if location is None:
            point(element.x, element.y)
        elif scale is None:
            # Why would you want to draw a point at a different location? Ever?
            point(location.x, location.y)
    elif isinstance(element, Ray):
        # Like a line, but it has an arrow at the end.
        # Might be the only shape element that uses location and scale.

        element =  element.clone()  # Clone the ray to avoid modifying the original.
        element.p2 *= scale if scale is not None else Size(1, 1)
        element.p1 += location if location is not None else Point(0, 0)
    
        line(*element.p1, *element.p2)
        angle = element.p2.angleTo(element.p1)
        line(
            element.p2.x,
            element.p2.y,
            element.p2.x + 10 * cos(angle + 0.5),
            element.p2.y + 10 * sin(angle + 0.5)
            )
        line(
            element.p2.x,
            element.p2.y,
            element.p2.x + 10 * cos(angle - 0.5),
            element.p2.y + 10 * sin(angle - 0.5)
            )

    elif isinstance(element, Line):
        # When including location and scale the math should be done from the midpoint of the line.
        if location is None and scale is None:
            line(*element.p1, *element.p2)
        elif location is not None and scale is not None:
            mid = element.midpoint()
            line(
                location.x + (element.p1.x - mid.x) * scale.width,
                location.y + (element.p1.y - mid.y) * scale.height,
                location.x + (element.p2.x - mid.x) * scale.width,
                location.y + (element.p2.y - mid.y) * scale.height
                )
        elif location is not None:
            mid = element.midpoint()    
            line(*(element.p1 - mid), *(element.p2 - mid))
        elif scale is not None:
            mid = element.midpoint()
            line(
                (element.p1.x - mid.x) * scale.width,
                (element.p1.y - mid.y) * scale.height,
                (element.p2.x - mid.x) * scale.width,
                (element.p2.y - mid.y) * scale.height
                )

    elif isinstance(element, Rect):
        rect(*element.pos, *element.size, edge)
        
    elif isinstance(element, Ellipse) or isinstance(element, Circle):
        ellipse(*element.pos, *element.size)

    elif isinstance(element, Triangle):
        triangle(*element.p1, *element.p2, *element.p3)

    elif isinstance(element, Sprite):
        if location is not None:
            if scale is not None:
                element.drawAt(location.x, location.y, scale.width, scale.height)
            else:
                element.drawAt(location.x, location.y, element.img.get_width(), element.img.get_height())
        else:
            raise DrawingError("Sprite must be drawn at a specific location and size.")
        
    elif isinstance(element, Image):
        if location is not None:
            element.transform(location.x, location.y, element.rect.size.width, element.rect.size.height)
        else:
            element.transform(element.rect.pos.x, element.rect.pos.y, element.rect.size.width, element.rect.size.height)
        element.draw(angle=angle)

    elif isinstance(element, Text):
        if location is not None:
            element.draw(location.x, location.y)
        else:
            element.draw(canvas.width/2, canvas.height/2)

    elif isinstance(element, Button):
        if location is not None:
            old_rect = element.rect
            element.rect.become(Rect(location, element.rect.size))
            element.draw()
            element.rect = old_rect  # Restore the original rect
        else:
            element.draw()

    elif element is None:
        pass

    elif isinstance(element, Style):
        element.apply()

    else:
        raise DrawingError("Unsupported shape type: " + str(type(element)))
    
    # Restore old styles
    if oldFill is not None:
        fill(*oldFill)
    if oldStroke is not None:
        stroke(*oldStroke)
    if oldWeight is not None:
        strokeWeight(oldWeight)

def mousePoint() -> Point:
    """Returns the mouse position as a Point object."""
    return Point(mouse.x, mouse.y)

def mouseLine() -> Line:
    """Returns the mouse position as a Point object."""
    return Line(Point(mouse.x, mouse.y), Point(pmouse.x, pmouse.y))

def averageAngles(angles:list[float]) -> float:
    """Averages a list of angles in radians."""
    x = sum(cos(a) for a in angles) / len(angles)
    y = sum(sin(a) for a in angles) / len(angles)
    return atan2(y, x)

_mouseRayAngles = []
def mouseRay() -> Ray:
    """Returns the mouse position as a Ray object."""
    _mouseRayAngles.append(mouseAngle())
    if len(_mouseRayAngles) > 30:
        _mouseRayAngles.pop(0)
    return Ray(Point(mouse.x, mouse.y), averageAngles(_mouseRayAngles)) # Average the last some angles to smooth out the ray.

stringifyUnits = ["", "Thousand", "Million", "Billion", "Trillion", "Quadrillion", "Quintillion", "Sextillion", "Septillion", "Octillion", "Nonillion", "Decillion", "Undecillion", "Duodecillion", "Tredecillion", "Quattuordecillion", "Quindecillion", "Sexdecillion", "Septendecillion", "Octodecillion", "Novemdecillion", "Vigintillion", "Unvigintillion", "Duovigintillion", "Trevigintillion", "Quattuorvigintillion", "Quinvigintillion", "Sexvigintillion", "Septenvigintillion", "Octovigintillion", "Novemvigintillion", "Trigintillion"]
def prefixNumber1(num:float|int) -> str:
    """Converts a number to a string, prefixes with 'thousand' or 'million' and so on if necessary. Always shows 4 digits, such as 1.234 Thousand / 12.34 Thousand / 123.4 Thousand."""
    for i, unit in enumerate(stringifyUnits):
        if num < 10**(3*(i+1)):
            return str(num/(10**(3*i)))[:5] + " " + unit if unit else str(num/(10**(3*i)))[:5]
    raise ValueError("Number is too large to be prefixed with a unit. Maximum is " + stringifyUnits[-1] + ". Number: " + str(num))

def prefixNumber2(num:float|int) -> str:
    """Converts a number to a string, prefixes with letters A, B, C, etc rather than thousand, million, etc. Always shows 4 digits, such as 1.234 A / 12.34 B / 123.4 C. Overflows to A+ after Z."""
    for i in range(308):  # 10^308 is the largest number that can be represented in Python, so we can safely loop up to that.
        if num < 10**(3*(i+1)):
            return str(num/(10**(3*i)))[:5] + " " + chr(65 + i%26) + ("+"*int(i/26))
    return "Infinity"  # If the number is too large, return "Infinity"

def colorAt(x:int, y:int) -> Color:
    """Returns the color of the pixel at the given coordinates."""
    if x < 0 or y < 0 or x >= canvas.width or y >= canvas.height:
        raise DrawingError("Coordinates out of bounds.")
    return Color(*canvas.screen.get_at((x, y))[:3])

def getPromptOutput(channel: str = "default", clear: bool = False) -> str:
    global prompt_outputs
    result = prompt_outputs.get(channel, "")
    if clear:
        prompt_outputs[channel] = ""
    return result

def promptOutputExists(channel: str = "default") -> bool:
    global prompt_outputs
    return channel in prompt_outputs and prompt_outputs[channel] != ""

paused:bool = False

pTime = time.time()
def dt(multi:float = 1) -> float:
    """Returns the delta time since the last frame in seconds, multiplied by the given multiplier."""
    return (time.time() - pTime) * multi

def activate() -> None:
    """Pauses the canvas."""
    global paused
    paused = True

def deactivate() -> None:
    """Unpauses the canvas."""
    global paused
    paused = False

def kill() -> None:
    """Kills the canvas."""
    exit()

prompt_outputs:dict[str, str] = {"default": "You stored nothing here yet."}
prompting:bool = False
current_prompt_channel:str = "default"
current_prompt:str = ""
prompt_input:str = ""
screen_before_prompt:pygame.surface.Surface = None
def startprompt(prompt:str = "Enter:", channel:str = "default") -> None:
    """Prompts the user for input. Stores it in "prompt_output" when the user presses enter.
    Everything is paused during this time, and prompt_output can only be accessed on the next frame."""
    global prompting, current_prompt, prompt_input, _lastkey, current_prompt_channel, prompt_outputs, screen_before_prompt
    prompting = True
    current_prompt = prompt
    current_prompt_channel = channel
    prompt_input = ""
    _lastkey = None  # Reset last key to avoid confusion with the prompt input.
    screen_before_prompt = canvas.screen.copy()  # Save the current screen before prompting.

def startprompt(prompt:str = "Enter:", channel:str = "default") -> None:
    """Prompts the user for input. Stores it in "prompt_output" when the user presses enter.
    Everything is paused during this time, and prompt_output can only be accessed on the next frame."""
    global prompting, current_prompt, prompt_input, _lastkey, current_prompt_channel, prompt_outputs, screen_before_prompt
    prompting = True
    current_prompt = prompt
    current_prompt_channel = channel
    prompt_input = ""
    _lastkey = None  # Reset last key to avoid confusion with the prompt input.
    screen_before_prompt = canvas.screen.copy()  # Save the current screen before prompting.

def start(activeloop:function, inactiveloop:function=nothing, eventhandler:function=nothing) -> None:
    """Starts the canvas. Has two loops, one for when the canvas is active and one for when it is inactive."""
    Style.default().apply()
    def draw():
        global paused, pTime, prompting, current_prompt, prompt_input
        if not paused and not prompting:
            activeloop()
            for button in IButton.all:
                button.tick()
        elif prompting:
            background(0, 0, 0)

            old_fill = fill(0,0,0)
            old_stroke = stroke(255,255,255)
            old_weight = strokeWeight(1)

            center = Point(canvas.width/2, canvas.height/2)
            rect(center.x - 200, center.y - 50, 400, 100, 10)

            textSize(20)
            fill(255, 255, 255)
            textAlign("LEFT", "CENTER")
            text(current_prompt, center.x - 190, center.y - 10)
            text(prompt_input, center.x - 190, center.y + 20)

            circle(center.x + sin(time.time() * 5) * 180, center.y - 50, 3)
            lastkey = lastKeyPressed()

            if keyboard.isDown(K.BACKSPACE):
                if len(prompt_input) > 0:
                    prompt_input = prompt_input[:-1]
            elif keyboard.isDown(K.ENTER):
                prompt_outputs[current_prompt_channel] = prompt_input
                prompting = False
                # Restore the screen before prompting.
                canvas.screen.blit(screen_before_prompt, (0, 0))
            elif lastkey:
                prompt_input += lastkey

            fill(*old_fill)
            stroke(*old_stroke)
            strokeWeight(old_weight)
        else:
            inactiveloop()
        pTime = time.time()
    Pycessing_run(draw, event_handler=eventhandler)