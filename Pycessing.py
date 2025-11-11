from __future__ import annotations
import pygame
import math
import random as r
import time
import os

hasSetup = False

class Canvas:
    """Class to handle the size of the display canvas."""
    def __init__(self, width:int, height:int):
        self.width = width
        self.height = height

    def __str__(self):
        return f"Size({self.width}, {self.height})"

    def __repr__(self):
        return self.__str__()
    
    def __iter__(self):
        """Allows iteration over the canvas object."""
        yield self.width
        yield self.height
    
    def surface(self) -> pygame.Surface:
        """Returns the surface of the canvas."""
        return _screen
    
    @property
    def center(self) -> tuple[int, int]:
        """Returns the center point of the canvas."""
        return (self.width // 2, self.height // 2)
    
    @property
    def screen(self) -> pygame.Surface:
        """Returns the screen surface."""
        return _screen

canvas = Canvas(0, 0)  # Default size
_start_time = int(time.time() * 1000)  # Start time in milliseconds
_framerate = 60  # Default frame rate
_screen = None  # The main display surface

def setup(TITLE:str, WIDTH:int = None, HEIGHT:int = None, framerate:int = 60) -> None:
    global _screen, width, height, hasSetup, _framerate
    """
    This function is used to configure the initial settings of the Pycessing environment.
    """
    if WIDTH is None and HEIGHT is None:
        _screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        canvas.width = pygame.display.Info().current_w
        canvas.height = pygame.display.Info().current_h
    else:
        _screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
        canvas.width = WIDTH
        canvas.height = HEIGHT
    pygame.display.set_caption(TITLE)
    _framerate = framerate
    hasSetup = True

try:
    # Initialize Pygame (this is done at the module level)
    pygame.init()
    pygame.font.init()  # Initialize the font module

    # Default background color
    _background_color = (200, 200, 200)  # Light gray

    # Store drawing settings
    _stroke_color:tuple = (0, 0, 0)  # Black
    _stroke_weight:int = 1
    _fill_color:tuple = (255, 255, 255)  # White
    _no_stroke:bool = False
    _no_fill:bool = False
    _rect_mode:str = "CORNER"  # CORNER, CENTER, CORNERS
    _ellipse_mode:str = "CENTER" # CENTER, CORNER, CORNERS, RADIUS
    _text_horizontal_align:str = "LEFT"  # LEFT, CENTER, RIGHT
    _text_vertical_align:str = "TOP"  # TOP, CENTER, BOTTOM
    _offset_x:int = 0
    _offset_y:int = 0

    # Stores pygame's key object as a local variable (the thing with key code constants)
    class K:
        """Class to handle key constants."""
        BACKSPACE = pygame.K_BACKSPACE  
        ENTER = pygame.K_RETURN
        RETURN = pygame.K_RETURN
        TAB = pygame.K_TAB
        ESCAPE = pygame.K_ESCAPE
        SPACE = pygame.K_SPACE
        PERIOD = pygame.K_PERIOD; COMMA = pygame.K_COMMA
        SEMICOLON = pygame.K_SEMICOLON; COLON = pygame.K_COLON
        QUOTE = pygame.K_QUOTE; APOSTROPHE = pygame.K_QUOTE
        HASH = pygame.K_HASH; DOLLAR = pygame.K_DOLLAR
        PERCENT = pygame.K_PERCENT; CARET = pygame.K_CARET
        AMPERSAND = pygame.K_AMPERSAND; STAR = pygame.K_ASTERISK
        LEFT_PAREN = pygame.K_LEFTPAREN; RIGHT_PAREN = pygame.K_RIGHTPAREN
        MINUS = pygame.K_MINUS; UNDERSCORE = pygame.K_UNDERSCORE
        PLUS = pygame.K_PLUS; EQUALS = pygame.K_EQUALS
        LEFT_BRACKET = pygame.K_LEFTBRACKET; RIGHT_BRACKET = pygame.K_RIGHTBRACKET
        BACKSLASH = pygame.K_BACKSLASH; SLASH = pygame.K_SLASH
        SHIFT = pygame.K_LSHIFT; CONTROL = pygame.K_LCTRL; ALT = pygame.K_LALT

        A = pygame.K_a; B = pygame.K_b; C = pygame.K_c; D = pygame.K_d; E = pygame.K_e; F = pygame.K_f; G = pygame.K_g
        H = pygame.K_h; I = pygame.K_i; J = pygame.K_j; K = pygame.K_k; L = pygame.K_l; M = pygame.K_m; N = pygame.K_n
        O = pygame.K_o; P = pygame.K_p; Q = pygame.K_q; R = pygame.K_r; S = pygame.K_s; T = pygame.K_t; U = pygame.K_u
        V = pygame.K_v; W = pygame.K_w; X = pygame.K_x; Y = pygame.K_y; Z = pygame.K_z

        UP = pygame.K_UP; DOWN = pygame.K_DOWN; LEFT = pygame.K_LEFT; RIGHT = pygame.K_RIGHT

        PAGE_UP = pygame.K_PAGEUP; PAGE_DOWN = pygame.K_PAGEDOWN

        HOME = pygame.K_HOME; END = pygame.K_END

        INSERT = pygame.K_INSERT; DELETE = pygame.K_DELETE

        PRINT_SCREEN = pygame.K_PRINTSCREEN; SCROLL_LOCK = pygame.K_SCROLLOCK

        PAUSE = pygame.K_PAUSE; BREAK = pygame.K_BREAK
        CAPS_LOCK = pygame.K_CAPSLOCK
        NUM_LOCK = pygame.K_NUMLOCK
        F1 = pygame.K_F1; F2 = pygame.K_F2; F3 = pygame.K_F3; F4 = pygame.K_F4
        F5 = pygame.K_F5; F6 = pygame.K_F6; F7 = pygame.K_F7; F8 = pygame.K_F8
        F9 = pygame.K_F9; F10 = pygame.K_F10; F11 = pygame.K_F11; F12 = pygame.K_F12

    class Mouse:
        """Class to handle mouse events and states."""
        def __init__(self, isMainMouse:bool = False) -> None:
            self._x:int = 0
            self._y:int = 0
            self._left:bool = False
            self._middle:bool = False
            self._right:bool = False
            self._mainMouse:bool = isMainMouse
            self._scrolled:int = 0  # Mouse wheel scroll value
        
        def __iter__(self):
            """Allows iteration over the mouse object."""
            yield self._x
            yield self._y

        @property
        def x(self):
            """x-coordinate of the mouse."""
            return self._x

        @property
        def y(self):
            """y-coordinate of the mouse."""
            return self._y

        @property
        def down(self):
            return self._left or self._middle or self._right

        @property
        def left(self):
            return self._left

        @property
        def middle(self):
            return self._middle

        @property
        def right(self):
            return self._right

        @property
        def scrolled(self):
            return self._scrolled
        
        @scrolled.setter
        def scrolled(self, value:int):
            """Sets the mouse wheel scroll value."""
            self._scrolled = value

        @property
        def pos(self):
            """Returns the current mouse position as a tuple (x, y)."""
            return (self._x, self._y)
        
        @pos.setter
        def pos(self, position:tuple[int,int]):
            """Sets the x-coordinate of the mouse.  Not recommended."""
            self._x = position[0]
            self._y = position[1]
            if self._mainMouse:
                pygame.mouse.set_pos(*position)

        @x.setter
        def x(self, xpos:int):
            """x-coordinate of the mouse."""
            self._x = xpos
            pygame.mouse.set_pos(xpos, self._y)
        
        @y.setter
        def y(self, ypos:int):
            """x-coordinate of the mouse."""
            self._y = ypos
            pygame.mouse.set_pos(self._x, ypos)
        
        @left.setter
        def left(self, pressed:bool):
            """Sets the left mouse button state."""
            self._left = pressed
        
        @middle.setter
        def middle(self, pressed:bool):
            """Sets the middle mouse button state."""
            self._middle = pressed
        
        @right.setter
        def right(self, pressed:bool):
            """Sets the right mouse button state."""
            self._right = pressed
        
        def hide(self) -> None:
            """Hides the mouse cursor."""
            pygame.mouse.set_visible(False)

        def show(self) -> None:
            """Shows the mouse cursor."""
            pygame.mouse.set_visible(True)

        def update(self) -> None:
            """Updates the mouse state."""
            self._x, self._y = pygame.mouse.get_pos()
            self._left, self._middle, self._right = pygame.mouse.get_pressed()
        
        def copy(self) -> Mouse:
            """Returns a copy of the current mouse state."""
            m = Mouse()
            m._x = self._x
            m._y = self._y
            m._left = self._left
            m._middle = self._middle
            m._right = self._right
            m._scrolled = self._scrolled
            return m
        
        def become(self, other:Mouse) -> None:
            """Sets the current mouse state to another mouse state."""
            self._x = other._x
            self._y = other._y
            self._left = other._left
            self._middle = other._middle
            self._right = other._right

        def loop(self, top:bool = True, right:bool = True, bottom:bool = True, left:bool = True, sensitivity:int = 2, centrality:int = -1) -> int:
            """
            Loops the mouse position around the screen edges.
            Return 0 for top, 1 for right, 2 for down, and 3 for left if the mouse looped through there.
            It can be specified which edges are allowed to be looped.
            Returns None if no loop occurred.
            Args:
                top: Allow looping through the top edge.
                right: Allow looping through the right edge.
                bottom: Allow looping through the bottom edge.
                left: Allow looping through the left edge.
                sensitivity: The distance from the edge to trigger the loop.
                centrality: How much from the center the mouse should be to trigger the loop.
            """
            
            if mouse.x < sensitivity and left                     and ((centrality == -1) or (abs(mouse.y - canvas.height / 2) < centrality)):
                mouse.x += canvas.width - 4
                return 3
            elif mouse.x > canvas.width - sensitivity and right   and ((centrality == -1) or (abs(mouse.y - canvas.height / 2) < centrality)):
                mouse.x -= canvas.width - sensitivity*2
                return 1
            elif mouse.y < sensitivity and top                    and ((centrality == -1) or (abs(mouse.x - canvas.width / 2) < centrality)):
                mouse.y += canvas.height - sensitivity*2
                return 0
            elif mouse.y > canvas.height - sensitivity and bottom and ((centrality == -1) or (abs(mouse.x - canvas.width / 2) < centrality)):
                mouse.y -= canvas.height - sensitivity*2
                return 2
            return None
        
        def pixelAt(self):
            """
            Returns the color of the pixel at the current mouse position.
            Returns a tuple (R, G, B) or None if the position is out of bounds.
            """
            if 0 <= self._x < canvas.width and 0 <= self._y < canvas.height:
                return _screen.get_at((self._x, self._y))[:3]

    class Keyboard:
        """Class to handle keyboard events and states."""
        def __init__(self) -> None:
            self.keys:pygame.key.ScancodeWrapper = pygame.key.get_pressed()

        def update(self) -> None:
            """Updates the keyboard state."""
            self.keys = pygame.key.get_pressed()

        def isDown(self, key:str|int) -> bool:
            """Checks if a specific key is currently pressed."""
            if isinstance(key, str):
                try:
                    return self.keys[ord(key)]
                except:
                    return False
            elif isinstance(key, int):
                return self.keys[key]
            return False

        def copy(self) -> Keyboard:
            """Returns a copy of the current keyboard state."""
            k = Keyboard()
            k.keys = pygame.key.ScancodeWrapper(self.keys)  # Copy the keys state
            return k
        
        def become(self, other:Keyboard) -> None:
            """Sets the current keyboard state to another keyboard state."""
            self.keys = pygame.key.ScancodeWrapper(other.keys)  # Copy the keys state

    mouse = Mouse(isMainMouse = True)  # Create a global mouse object
    pmouse = Mouse()  # Previous mouse state
    ppmouse = Mouse() # Previous previous mouse state
    keyboard = Keyboard()  # Create a global keyboard object
    pkeyboard = Keyboard() # Previous keyboard state
    ppkeyboard = Keyboard() # Previous previous keyboard state

    # --- Helper Functions ---

    def _convert_color(color) -> tuple[int, int, int]:
        """
        Converts various color formats to RGB tuples.
        Handles:
            - RGB tuples (e.g., (255, 0, 0))
            - Single grayscale values (e.g., 100)
            - Hex color strings (e.g., "#FF0000")
        """
        if isinstance(color, tuple):
            return (constrain(color[0], 0, 255), constrain(color[1], 0, 255), constrain(color[2], 0, 255))
        elif isinstance(color, int):
            return (constrain(color, 0, 255), constrain(color, 0, 255), constrain(color, 0, 255))  # Grayscale
        elif isinstance(color, str):
            if color.startswith("#"):
                return tuple(int(color[i:i+2], 16) for i in (1, 3, 5))
            else:
                raise ValueError(f"Invalid color string: {color}")
        else:
            raise TypeError(f"Invalid color type: {type(color)}")

    def _handle_rect_mode(x, y, width, height) -> tuple[int, int, int, int]:
        """
        Handles different rectMode settings.  Returns x, y, width, height.
        """
        if _rect_mode == "CENTER":
            x -= width / 2
            y -= height / 2
        elif _rect_mode == "CORNERS":
            width -= x
            height -= y
        return int(x), int(y), int(width), int(height)

    def _handle_ellipse_mode(x, y, a, b) -> tuple[int, int, int, int]:
        """
        Handles different ellipseMode settings. Returns x, y, a, b.
        """
        if _ellipse_mode == "CORNER":
            x += a / 2
            y += b / 2
        elif _ellipse_mode == "CORNERS":
            a -= x
            b -= y
            x += a / 2
            y += b / 2
        elif _ellipse_mode == "RADIUS":
            a *= 2
            b *= 2
        elif _ellipse_mode == "CENTER":
            x -= a / 2
            y -= b / 2  
        return int(x), int(y), int(a), int(b)

    # --- Drawing Functions ---

    def background(*args) -> None:
        """
        Sets the background color of the display canvas.

        Args:
            color: The color to set the background to. Can be an RGB tuple,
                a grayscale value, or a hex color string.
        """
        global _background_color
        if len(args) == 1:
            _background_color = _convert_color(args[0])
        elif len(args) == 3:
            _background_color = _convert_color((args[0], args[1], args[2]))
        else:
            raise ValueError(f"Invalid background arguments: {args}")
        _screen.fill(_background_color)

    def size(w, h) -> None:
        """
        Sets the size of the display canvas.

        Args:
            width: The width of the canvas in pixels.
            height: The height of the canvas in pixels.
        """
        global width, height, _screen
        width = w
        height = h
        _screen = pygame.display.set_mode((w, h))
        # Preserve the old background by redrawing it after resizing.
        _screen.fill(_background_color)  # Redraw the previous background color.

    def fill(*args) -> tuple[int, int, int]:
        """
        Sets the fill color for subsequent drawing operations. Returns the original fill color.

        Returns:
            The original fill color as an RGB tuple.
        Args:
            color: The fill color. Can be an RGB tuple, grayscale value, or hex string.
        """
        global _fill_color, _no_fill

        original_fill_color = _fill_color

        if len(args) == 1:
            _fill_color = _convert_color(args[0])
        elif len(args) == 3:
            _fill_color = _convert_color((args[0], args[1], args[2]))
        else:
            raise ValueError(f"Invalid fill arguments: {args}")
        _no_fill = False

        return original_fill_color
    
    def getFill() -> tuple[int, int, int]:
        """
        Returns the current fill color.
        """
        return _fill_color

    def noFill() -> None:
        """
        Disables filling for subsequent drawing operations.
        """
        global _no_fill
        _no_fill = True

    def stroke(*args) -> None:
        """
        Sets the stroke (outline) color for subsequent drawing operations.

        Returns:
            The original stroke color before setting the new one.
        Args:
            color: The stroke color.  Can be an RGB tuple, grayscale value, or hex string.
        """
        global _stroke_color, _no_stroke
        original_stroke_color = _stroke_color

        if len(args) == 1:
            _stroke_color = _convert_color(args[0])
        elif len(args) == 3:
            _stroke_color = _convert_color((args[0], args[1], args[2]))
        else:
            raise ValueError(f"Invalid stroke arguments: {args}")
        _no_stroke = False

        return original_stroke_color
    
    def getStroke() -> tuple[int, int, int]:
        """
        Returns the current stroke color.
        """
        return _stroke_color

    def noStroke() -> None:
        """
        Disables the stroke (outline) for subsequent drawing operations.
        """
        global _no_stroke, _stroke_weight
        _no_stroke = True
        _stroke_weight = 0  # Set stroke weight to 0 when noStroke is called

    def strokeWeight(weight:int) -> int:
        """
        Sets the stroke (outline) thickness for subsequent drawing operations.

        Returns:
            The original stroke weight before setting the new one.
        Args:
            weight: The thickness of the stroke in pixels.
        """
        global _stroke_weight, _no_stroke
        original_weight = _stroke_weight

        _stroke_weight = int(weight)  # Ensure it's an integer
        _no_stroke = False  # Enable stroke if it was previously disabled

        return original_weight
    
    def getStrokeWeight() -> int:
        """
        Returns the current stroke weight.
        """
        return _stroke_weight

    def rectMode(mode:str) -> None:
        """
        Sets the mode for interpreting the parameters of the rect() function.
        Valid modes are: "CORNER", "CENTER", and "CORNERS".
        """
        global _rect_mode
        mode = mode.upper()
        if mode in ("CORNER", "CENTER", "CORNERS"):
            _rect_mode = mode
        else:
            raise ValueError(f"Invalid rectMode: {mode}.  Must be CORNER, CENTER, or CORNERS")

    def ellipseMode(mode:str) -> None:
        """
        Sets the mode for interpreting the parameters of the ellipse() function.
        Valid modes are: "CENTER", "CORNER", "CORNERS", and "RADIUS".
        """
        global _ellipse_mode
        mode = mode.upper()
        if mode in ("CENTER", "CORNER", "CORNERS", "RADIUS"):
            _ellipse_mode = mode
        else:
            raise ValueError(f"Invalid ellipseMode: {mode}. Must be CENTER, CORNER, CORNERS, or RADIUS")
        
    def rect(x:int, y:int, width:int, height:int, corner_radius:int=0) -> None:
        """
        Draws a rectangle to the display canvas.

        Args:
            x: The x-coordinate of the rectangle.
            y: The y-coordinate of the rectangle.
            width: The width of the rectangle.
            height: The height of the rectangle.
        """
        x, y, width, height = _handle_rect_mode(x, y, width, height)

        if not _no_fill:
            pygame.draw.rect(_screen, _fill_color, (x, y, width, height), border_radius=corner_radius)
        if not (_no_stroke or _stroke_weight == 0):
            pygame.draw.rect(_screen, _stroke_color, (x, y, width, height), _stroke_weight, border_radius=corner_radius)

    def ellipse(x:int, y:int, a:int, b:int):
        """
        Draws an ellipse (or circle) to the display canvas.

        Args:
            x: The x-coordinate of the ellipse's center (or corner, depending on ellipseMode).
            y: The y-coordinate of the ellipse's center (or corner, depending on ellipseMode).
            a: The width (diameter) of the ellipse.
            b: The height (diameter) of the ellipse.
        """
        x, y, a, b = _handle_ellipse_mode(x, y, a, b)
        if not _no_fill:
            pygame.draw.ellipse(_screen, _fill_color, (x, y, a, b))
        if not _no_stroke:
            pygame.draw.ellipse(_screen, _stroke_color, (x, y, a, b), _stroke_weight)

    def circle(x:int, y:int, r:int):
        """
        Draws a circle to the display canvas.  Equivalent to ellipse(x, y, 2r, 2r).

        Args:
            x: The x-coordinate of the circle's center.
            y: The y-coordinate of the circle's center.
            r: The radius of the circle.
        """
        ellipse(x, y, 2 * r, 2 * r)  # Reuse ellipse

    def _curveStepLeft(p1:tuple[int,int], p2:tuple[int,int], p3:tuple[int,int]):
        # Calculate the centroid of the three points
        centroid_x = (p1[0] + p2[0] + p3[0]) / 3
        centroid_y = (p1[1] + p2[1] + p3[1]) / 3
        # Get the midpoint from p1 to p2
        mid_p1_p2_x = (p1[0] + p2[0]) / 2
        mid_p1_p2_y = (p1[1] + p2[1]) / 2
        # Double the distance from the midpoint of p1-p2 from the centroid
        x1 = centroid_x + (mid_p1_p2_x - centroid_x) * 2
        y1 = centroid_y + (mid_p1_p2_y - centroid_y) * 2
        # return both new points
        return (x1, y1)
    
    def _curveStepRight(p1:tuple[int,int], p2:tuple[int,int], p3:tuple[int,int]):
        # Calculate the centroid of the three points
        centroid_x = (p1[0] + p2[0] + p3[0]) / 3
        centroid_y = (p1[1] + p2[1] + p3[1]) / 3
        # Get the midpoint from p2 to p3
        mid_p2_p3_x = (p2[0] + p3[0]) / 2
        mid_p2_p3_y = (p2[1] + p3[1]) / 2
        # Double the distance from the midpoint of p2-p3 from the centroid
        x2 = centroid_x + (mid_p2_p3_x - centroid_x) * 2
        y2 = centroid_y + (mid_p2_p3_y - centroid_y) * 2
        # return both new points
        return (x2, y2)

    def curve(p1:tuple[int,int], p2:tuple[int,int], p3:tuple[int,int], iters:int = 5):
        if iters < 1:
            return [p1, p3]
        
        return curve(_curveStepLeft(p1, p2, p3), p2, p3, iters - 1) + curve(p1, p2, _curveStepRight(p1, p2, p3), iters - 1)

    def bezier(x1:int, y1:int, x2:int, y2:int, x3:int, y3:int):
        """
        Draws a Bezier curve.

        Args:
            x1: The x-coordinate of the first control point.
            y1: The y-coordinate of the first control point.
            x2: The x-coordinate of the second control point.
            y2: The y-coordinate of the second control point.
            x3: The x-coordinate of the third control point.
            y3: The y-coordinate of the third control point.
        """
        if not _no_stroke:
            pygame.draw.lines(_screen, _fill_color, False, curve((x1,y1), (x2, y2), (x3, y3)), width=_stroke_weight)
            

    def line(x1:int, y1:int, x2:int, y2:int, endcaps:bool=False):
        """
        Draws a line segment between two points.

        Args:
            x1: The x-coordinate of the first point.
            y1: The y-coordinate of the first point.
            x2: The x-coordinate of the second point.
            y2: The y-coordinate of the second point.
        """
        if not _no_stroke:
            pygame.draw.line(_screen, _stroke_color, (x1, y1), (x2, y2), _stroke_weight)
            if endcaps:
                radius = _stroke_weight // 2
                pygame.draw.circle(_screen, _stroke_color, (x1, y1), radius)
                pygame.draw.circle(_screen, _stroke_color, (x2, y2), radius)

    def point(x:int, y:int):
        """
        Draws a point (a very small rectangle) at the specified coordinates.

        Args:
            x: The x-coordinate of the point.
            y: The y-coordinate of the point.
        """
        if not _no_stroke:
            # Pygame doesn't have a single-pixel point, so we draw a tiny rect.
            pygame.draw.rect(_screen, _stroke_color, (x, y, _stroke_weight, _stroke_weight))



    def triangle(x1:int, y1:int, x2:int, y2:int, x3:int, y3:int):
        """
        Draws a triangle.

        Args:
        x1: The x coordinate of the first point.
        y1: The y coordinate of the first point.
        x2: The x coordinate of the second point.
        y2: The y coordinate of the second point.
        x3: The x coordinate of the third point.
        y3: The y coordinate of the third point.
        """
        points = [(x1, y1), (x2, y2), (x3, y3)]
        if not _no_fill:
            pygame.draw.polygon(_screen, _fill_color, points)
        if not _no_stroke:
            pygame.draw.polygon(_screen, _stroke_color, points, _stroke_weight)

    def quad(x1:int, y1:int, x2:int, y2:int, x3:int, y3:int, x4:int, y4:int):
        """
        Draws a quadrilateral.

        Args:
            x1: The x-coordinate of the first point.
            y1: The y-coordinate of the first point.
            x2: The x-coordinate of the second point.
            y2: The y-coordinate of the second point.
            x3: The x-coordinate of the third point.
            y3: The y-coordinate of the third point.
            x4: The x-coordinate of the fourth point.
            y4: The y-coordinate of the fourth point.
        """
        points = [(x1, y1), (x2, y2), (x3, y3), (x4, y4)]
        if not _no_fill:
            pygame.draw.polygon(_screen, _fill_color, points)
        if not _no_stroke:
            pygame.draw.polygon(_screen, _stroke_color, points, _stroke_weight)
    # --- Text Functions ---
    _font_name:str= 'C:/Windows/Fonts/calibri.ttf'
    _font:pygame.font.Font = pygame.font.Font('C:/Windows/Fonts/calibri.ttf', 12)
    _font_size = 12

    def createFont(name:str, size:int):
        """Creates a font object.  Must be called before using text().
            name can be a system font name, or a path to a .ttf or .otf file.
        """
        global _font, _font_size
        try:
            _font_name = name
            _font = pygame.font.Font(name, size)
        except pygame.error as e:
            print(f"Error creating font: {e}")
            _font = None # Set to None to indicate error
        _font_size = size

    def textSize(size:int):
        """
        Sets the size of the font.

        Note:
            `createFont` must be called before using this function. If `_font` is `None`,
            a warning will be printed, and the function will not proceed.
        """
        global _font, _font_size
        if _font is None:
            print("textSize() called before createFont()")
            return
        _font_size = size
        _font = pygame.font.Font(_font_name, _font_size) #Recreate the font.

    def text(string:str, x:int, y:int):
        """
        Draws text to the display canvas.  Requires create_font() to be called first.

        Args:
            raise RuntimeError("text() called before createFont(). Please call createFont() before using text().")
            y: The y-coordinate of the text's position.
        """
        if _font is None:
            print("text() called before create_font()")
            return  # Or raise an exception?

        text_surface = _font.render(string, True, _fill_color)  # Use _fill_color for text
        # correct the alignment based on _text_horizontal_align and _text_vertical_align
        _screen.blit(text_surface, (
            x - text_surface.get_width() // 2 if _text_horizontal_align == "CENTER" else
            x - text_surface.get_width() if _text_horizontal_align == "RIGHT" else x,
            y - text_surface.get_height() // 2 if _text_vertical_align == "CENTER" else
            y - text_surface.get_height() if _text_vertical_align == "BOTTOM" else y
        ))

    def textWidth(string:str) -> int:
        """Calculates the width of a given string in pixels, using the current font."""

        if _font is None:
            print("textwidth() called before create_font()")
            return 0
        return _font.size(string)[0]

    def textHeight(string) -> int:
        """Calculates the height of a given string in pixels, using the current font."""

        if _font is None:
            print("textheight() called before create_font()")
            return 0
        return _font.size(string)[1] # Full height of the text.
    
    def textAlign(horizontal:str = "LEFT", vertical:str = "TOP") -> None:
        """
        Sets the alignment for text rendering.

        Args:
            horizontal: Horizontal alignment. Can be "LEFT", "CENTER", or "RIGHT".
            vertical: Vertical alignment. Can be "TOP", "CENTER", or "BOTTOM".
        """
        global _text_horizontal_align, _text_vertical_align
        horizontal = horizontal.upper()
        vertical = vertical.upper()
        
        if horizontal in ("LEFT", "CENTER", "RIGHT"):
            _text_horizontal_align = horizontal
        else:
            raise ValueError(f"Invalid horizontal alignment: {horizontal}. Must be LEFT, CENTER, or RIGHT.")
        
        if vertical in ("TOP", "CENTER", "BOTTOM"):
            _text_vertical_align = vertical
        else:
            raise ValueError(f"Invalid vertical alignment: {vertical}. Must be TOP, CENTER, or BOTTOM.")

    # --- Input Functions ---

    def keyIsPressed(key:str|int) -> bool:
        """Checks if a specific key is currently pressed."""

        if isinstance(key, str):
            return keyboard.keys[ord(key)]
        elif isinstance(key, int):
            return keyboard.keys[key]

    def keyWasPressed(key:str|int) -> bool:
        """Checks if a specific key was pressed in the last frame."""
        
        if isinstance(key, str):
            return pkeyboard.keys[ord(key)]
        elif isinstance(key, int):
            return pkeyboard.keys[key]
    
    def keyReleased(key:str|int) -> bool:
        """ Checks if a specific key was released."""
        return (not keyboard.isDown(key)) and pkeyboard.isDown(key)
    
    def keyClicked(key:str|int) -> bool:
        """Checks if a specific key was clicked."""
        return keyboard.isDown(key) and (not pkeyboard.isDown(key))

    _lastKey:str = ""  # Store the last key pressed
    def lastKeyPressed() -> str:
        # Check every single ke
        for i in "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789.,;:!@#$%^&*()-_=+[]{}|\\`~":
            if keyClicked(i):
                _lastKey = i
                return i

    def mouseIsPressed(button:int=None) -> bool:
        """Checks if a specific mouse button is currently pressed."""
        if button == 1:
            return mouse.left
        elif button == 2:
            return mouse.middle
        elif button == 3:
            return mouse.right
        elif button is None:
            return mouse.left or mouse.middle or mouse.right
        else:
            raise ValueError(f"Invalid mouse button: {button}. Must be 1 (left), 2 (middle), or 3 (right).")
    
    def mouseWasPressed(button:int=None) -> bool:
        """Checks if a specific mouse button was pressed in the last frame."""
        if button == 1:
            return mouse.left and not pmouse.left
        elif button == 2:
            return mouse.middle and not pmouse.middle
        elif button == 3:
            return mouse.right and not pmouse.right
        elif button is None:
            return (mouse.left and not pmouse.left) or (mouse.middle and not pmouse.middle) or (mouse.right and not pmouse.right)
        else:
            raise ValueError(f"Invalid mouse button: {button}. Must be 1 (left), 2 (middle), or 3 (right).")
        
    def mouseReleased(button:int=None) -> bool:
        """Checks if a specific mouse button was released."""
        if button == 1:
            return not mouse.left and pmouse.left
        elif button == 2:
            return not mouse.middle and pmouse.middle
        elif button == 3:
            return not mouse.right and pmouse.right
        elif button is None:
            return (not mouse.left and pmouse.left) or (not mouse.middle and pmouse.middle) or (not mouse.right and pmouse.right)
        else:
            raise ValueError(f"Invalid mouse button: {button}. Must be 1 (left), 2 (middle), or 3 (right).")
    
    def mouseClicked(button:int=None) -> bool:
        """Checks if a specific mouse button was clicked."""
        if button == 1:
            return mouse.left and not pmouse.left
        elif button == 2:
            return mouse.middle and not pmouse.middle
        elif button == 3:
            return mouse.right and not pmouse.right
        elif button is None:
            return (mouse.left and not pmouse.left) or (mouse.middle and not pmouse.middle) or (mouse.right and not pmouse.right)
        else:
            raise ValueError(f"Invalid mouse button: {button}. Must be 1 (left), 2 (middle), or 3 (right).")

    # --- Timing Functions ---
    def millis() -> int:
        """Returns the number of milliseconds since the program started."""
        return int(time.time() * 1000) - _start_time

    # --- Math Functions ---

    def log(x:float, base:float = 10) -> float:
        """Calculates the logarithm of x to the specified base."""
        return math.log(x, base)
    
    def ln(x:float) -> float:
        """Calculates the natural logarithm (base e) of x."""
        return math.log(x)

    def remap(value:float, start1:float, stop1:float, start2:float, stop2:float) -> float:
        """Re-maps a number from one range to another."""
        return start2 + (stop2 - start2) * ((value - start1) / (stop1 - start1))

    def constrain(value:float, min_value:float, max_value:float) -> float:
        """
        Constrains a value to be within a minimum and maximum range.
        """
        return max(min(value, max_value), min_value)

    def dist(x1:float, y1:float, x2:float, y2:float) -> float:
        """Calculates the distance between two points."""
        return math.sqrt((x2 - x1)**2 + (y2 - y1)**2)

    def random(low:float=1.0, high:float=None):
        """
        Generates a random floating-point number.

        Args:
            low: The lowest possible value (inclusive).  If high is None,
                this is interpreted as the highest possible value.
            high: The highest possible value (exclusive).
        """
        if high is None:
            high = low
            low = 0.0
        return r.uniform(low, high)
    
    def frandom(low:float=1.0, high:float=None):
        """
        floored random number generator.
        """
        return int(random(low, high))

    def rand(low:float=1.0, high:float=None):
        """
        Generates a random floating-point number.

        Args:
            low: The lowest possible value (inclusive).  If high is None,
                this is interpreted as the highest possible value.
            high: The highest possible value (exclusive).
        """
        if high is None:
            high = low
            low = 0.0
        return r.uniform(low, high)
        return r.randint(low, high)

    def randomSign():
        """Returns a random sign (-1 or 1)."""
        return -1 if random(0, 1) < 0.5 else 1

    def number(x):
        """Converts a number to a float"""
        return float(x)

    # --- Trigonometry Functions ---
    def sin(angle):
        """
        Calculates the sine of an angle (in radians).
        """
        return math.sin(angle)

    def cos(angle):
        """
        Calculates the cosine of an angle (in radians).
        """
        return math.cos(angle)

    def tan(angle):
        """
        Calculates the tangent of an angle (in radians).
        """
        return math.tan(angle)

    def radians(degrees):
        """
        Converts an angle from degrees to radians.
        """
        return math.radians(degrees)

    def degrees(radians):
        """
        Converts an angle from radians to degrees.
        """
        return math.degrees(radians)

    def atan2(y, x):
        """
        Calculates the arctangent of y/x, taking into account the signs of both
        y and x to determine the correct quadrant. Returns value in radians.
        """
        return math.atan2(y, x)
    
    def sqrt(x):
        """
        Calculates the square root of a number.
        """
        return math.sqrt(x)
    
    def sq(x):
        """
        Calculates the square of a number.
        """
        return x * x

    # --- Image functions ---
    def load_image(filename):
        """Loads an image from a file.  Returns a Pygame Surface object, or None on error."""
        try:
            return pygame.image.load(os.path.join(os.path.dirname(os.path.abspath(__file__)), filename))
        except pygame.error as e:
            print(f"Error loading image: {e}")
            return None

    def image(img: pygame.Surface, x: int, y: int, width: int = None, height: int = None, angle: float = 0, flipX:bool = False, flipY:bool = False):
        """Draws an image to the screen, with optional scaling and rotation.

        Args:
            img: A Pygame Surface object (loaded with load_image).
            x: The x-coordinate of where to draw the image.
            y: The y-coordinate of where to draw the image.
            width: Optional width to scale the image.
            height: Optional height to scale the image.
            angle: Optional angle (in degrees) to rotate the image (clockwise).
        """
        if img is None:
            return  # Error was already reported in load_image

        draw_img = img
        
        if width is not None and height is not None:
            # scale after rotation to avoid distortion
            draw_img = pygame.transform.scale(draw_img, (width, height))

        if angle != 0:
            # Angle is in clockwise radians starting from the left -> converted to degrees started from the left going counter-clockwise
            new_width = abs(width * cos(angle)) + abs(height * sin(angle))
            new_height = abs(width * sin(angle)) + abs(height * cos(angle))
            pygame.transform.scale(draw_img, (new_width, new_height))
            draw_img = pygame.transform.rotate(draw_img, angle * -180 / math.pi + 180)

            # offset x and y by half the difference in the new and old dimensions
            x -= (new_width - width) // 2
            y -= (new_height - height) // 2
        
        if flipX or flipY:
            draw_img = pygame.transform.flip(draw_img, flipX, flipY)

        _screen.blit(draw_img, (x, y))

    # --- Sound functions ---
    def load_sound(filename):
        """Loads a sound from a file.  Returns a Pygame Sound object, or None on error."""
        try:
            return pygame.mixer.Sound(os.path.join(os.path.dirname(os.path.abspath(__file__)), filename))
        except pygame.error as e:
            print(f"Error loading sound: {e}")
            return None

    # --- Color functions ---
    def color(r:int, g:int=None, b:int=None):
        """
        Creates a color value.

        Args:
            r:  Red value (0-255) or grayscale value if g and b are None.
            g:  Green value (0-255).
            b:  Blue value (0-255).
            a:  Alpha value (0-255).
        """
        if g is None and b is None:
            return (r, r, r) # Grayscale
        else:
            return (r, g, b)

    def red(c):
        """Returns the red component of a color."""
        return c[0]

    def green(c):
        """Returns the green component of a color."""
        return c[1]

    def blue(c):
        """Returns the blue component of a color."""
        return c[2]

    def alpha(c):
        """Returns the alpha component of a color, or 255 if not present."""
        return c[3] if len(c) > 3 else 255

    def colorLerp(c1, c2, amount):
        """Linearly interpolates between two colors."""
        r1, g1, b1 = c1[:3]
        r2, g2, b2 = c2[:3]
        a1 = c1[3] if len(c1) > 3 else 255
        a2 = c2[3] if len(c2) > 3 else 255

        r = int(r1 + (r2 - r1) * amount)
        g = int(g1 + (g2 - g1) * amount)
        b = int(b1 + (b2 - b1) * amount)
        a = int(a1 + (a2 - a1) * amount)
        return (r, g, b, a)

    lerp_color = colorLerp

    class JSObject:
        def __init__(self, **kwargs):
            self.__dict__.update(kwargs)

        def __getattr__(self, name):
            # If the attribute doesn't exist, return None (like undefined in JS)
            return None if name not in self.__dict__.keys() else self.__dict__[name]

        def __setattr__(self, name, value):
            self.__dict__[name] = value

        def __delattr__(self, name):
            if name in self.__dict__:
                del self.__dict__[name]

        def keys(self):
            return self.__dict__.keys()

        def values(self):
            return self.__dict__.values()

        def items(self):
            return self.__dict__.items()

        def __repr__(self):
            """Returns a string representation of the object."""
            return f"JSObject({self.__dict__})"
        
        def __str__(self):
            return f"[object Object]"

    def default(*args, **kwargs):
        """
        A default function that does nothing.  Can be used as a placeholder.
        """
        pass

    _lastMouseAngle:float = 0.0

    def mouseAngle() -> float:
        """Returns the angle of the mouse movement in radians."""
        return _lastMouseAngle

    # --- Main Loop ---
    def Pycessing_run(draw_func:function, setup_func:function=None, event_handler:function=default):
        """
        Runs the main Pygame loop, calling draw_func repeatedly.  Optionally
        calls setup_func once at the beginning.

        Args:
            draw_func:  The function to call repeatedly to draw to the screen.
                        This function should take no arguments.
            setup_func: Optional function to call once at the beginning.  No arguments.
            event_handler: Optional function to handle Pygame events.  Takes the event
                        as an argument.  If not provided, default event handling
                        (checking for QUIT) is used.
        """

        # Get input
        global mouse, pmouse, ppmouse, keyboard, pkeyboard, ppkeyboard, _lastKey, _lastMouseAngle

        if setup_func:
            setup_func()

        running = True
        while running:
            if (ppmouse.x, ppmouse.y) != (mouse.x, mouse.y):
                _lastMouseAngle = atan2(mouse.y - ppmouse.y, mouse.x - ppmouse.x)

            ppmouse.become(pmouse)  # Copy the current state to ppmouse for mouseWasPressed
            pmouse.become(mouse)  # Copy the current state to pmouse for mouseWasPressed
            mouse.update()  # Update the mouse state
            ppkeyboard.become(pkeyboard)
            pkeyboard.become(keyboard)  # Copy the current state to pkeyboard for keyWasPressed
            keyboard.update()  # Update the keyboard state

            scrolled:bool = False
            for event in pygame.event.get():
                if event_handler:
                    event_handler(event)
                if event.type == pygame.KEYDOWN:
                    _lastKey = pygame.key.name(event.key)
                    if event.key == pygame.K_ESCAPE:
                        running = False
                elif event.type == pygame.MOUSEWHEEL:
                    mouse.scrolled = event.y
                    scrolled = True
                elif event.type == pygame.QUIT:
                    running = False
            
            if not scrolled:
                mouse.scrolled = 0

            # _screen.fill(_background_color)  # Clear the background each frame
            draw_func()
            pygame.display.flip()
            pygame.time.Clock().tick(_framerate)  # Cap frame rate at 60 FPS (adjust as needed)
        pygame.quit()
except Exception as e:
    # current device does not support running in IDE so must be run through python for error 
    input(e)