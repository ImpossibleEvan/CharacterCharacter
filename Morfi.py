from __future__ import annotations
from typing import Union
from time import time as now
import math

"""
Morfi is a library of geometric classes and functions.
Morfi is a Greek word meaning "shape".
Some other useful tools are found in here as well.

"""

def average(*args) -> float:
    return sum(args) / len(args)

def between(MIN:int|float, VAL:int|float, MAX:int|float) -> bool:
    return MIN <= VAL <= MAX

class dualmethod:
    """Decorator to make a method callable from both the class and the instance.
    To use, decorate a method with @dualmethod and define the first argument as 'cls'.
    Then the SECOND argument will be the self when called from an instance."""

    def __init__(self, func):
        self.func = func

    def __get__(self, instance, owner):
        if instance is None:
            # Called from class
            def method(*args, **kwargs):
                return self.func(owner, *args, **kwargs)
        else:
            # Called from instance
            def method(*args, **kwargs):
                return self.func(owner, instance, *args, **kwargs)
        return method

class Infinitesimal:
    """A class to represent an infinitesimal value, useful for comparing floating point numbers."""
    def __init__(self, precision:float = 0):
        self.precision = 0.1**precision
    def __eq__(self, value):
        return -self.precision < value < self.precision
    def __ne__(self, value):
        return not self.__eq__(value)
zero = Infinitesimal()

class Interval:
    """A class to represent an interval of numbers."""
    def __init__(self, start:int, end:int):
        self.start = int(min(start, end))
        self.end = int(max(start, end))

    def __iter__(self):
        yield self.start
        yield self.end

    def __contains__(self, value:Number|Interval) -> bool:
        """Checks if a value is in the interval or if the interval overlaps with the other interval."""
        if isinstance(value, Interval):
            return self.start <= value.start <= self.end or self.start <= value.end <= self.end or value.start <= self.start <= value.end or value.start <= self.end <= value.end
        elif isinstance(value, Number):
            return self.start <= value <= self.end
    
    def overlaps(self, other:Interval) -> bool:
        """Checks if the interval overlaps with another interval."""
        return self in other or other in self

    def __len__(self) -> int:
        """Returns the length of the interval as an int"""
        return int(self.end - self.start)

    def clone(self) -> Interval:
        """Returns a deep copy of the Interval."""
        return Interval(self.start, self.end)

    def __repr__(self):
        return f"Interval({self.start}, {self.end})"
    
    def __getitem__(self, index:int) -> int:
        """Returns the start or end of the interval."""
        if index == 0:
            return self.start
        elif index == 1:
            return self.end
        else:
            raise IndexError("Index out of range for Interval. Use 0 for start and 1 for end.")
    
    def __eq__(self, other:Interval) -> bool:
        """Checks if two intervals are equal."""
        if not isinstance(other, Interval):
            return False
        return self.start == other.start and self.end == other.end
    
    def __ne__(self, other:Interval) -> bool:
        """Checks if two intervals are not equal."""
        return not self.__eq__(other)
    
    def __hash__(self):
        """Returns a hash of the interval."""
        return hash((self.start, self.end))

class Pair:
    def __init__(self, first, second):
        self.first:int = int(first)
        self.second:int = int(second)
    
    def clone(self) -> Pair:
        """Returns a deep copy of the Pair"""
        return Pair(self.first, self.second)

    def __repr__(self):
        return f"Pair({self.first}, {self.second})"

    def __eq__(self, other):
        return self.first == other.first and self.second == other.second
    
    def __ne__(self, other):
        return not self.__eq__(other)

    def __hash__(self):
        return hash((self.first, self.second))
    
    def __iter__(self):
        yield self.first
        yield self.second
    
    def __getitem__(self, index:int) -> int:
        """Returns the first or second element of the Pair"""
        if index == 0:
            return self.first
        elif index == 1:
            return self.second
        else:
            raise IndexError("Index out of range for Pair. Use 0 for first and 1 for second.")

class Size:
    def __init__(self, width:int, height:int):
        self.width:int = int(width)
        self.height:int = int(height)

    def __iter__(self):
        yield self.width
        yield self.height

    def __getitem__(self, index:int) -> int:
        """Returns the width or height of the Size"""
        return self.width if index == 0 else self.height
    
    def area(self) -> int:
        """Returns the area of the Size"""
        return self.width * self.height
    
    def perimeter(self) -> int:
        """Returns the perimeter of the Size"""
        return 2 * (self.width + self.height)
    
    def clone(self) -> Size:
        """Returns a deep copy of the Size"""
        return Size(self.width, self.height)

    def __add__(self, other:Size):
        return Size(self.width + other.width, self.height + other.height)
    
    def __sub__(self, other:Size):
        return Size(self.width - other.width, self.height - other.height)
    
    def __mul__(self, other:int|float):
        return Size(self.width * other, self.height * other)
    
    def __truediv__(self, other:int|float):
        return Size(self.width / other, self.height / other)
    
    def __str__(self):
        return f"{self.width} by {self.height}"
    
    def __repr__(self):
        return f"Size({self.width}, {self.height})"
    
    def __eq__(self, other:Size) -> bool:
        return self.width == other.width and self.height == other.height
    
    def __ne__(self, other:Size) -> bool:
        return not self.__eq__(other)
    
    def __lt__(self, other:Size) -> bool:
        return self.width*self.height < other.width*other.height
    
    def __le__(self, other:Size) -> bool:
        return self.width*self.height <= other.width*other.height
    
    def __gt__(self, other:Size) -> bool:
        return self.width*self.height > other.width*other.height
    
    def __ge__(self, other:Size) -> bool:
        return self.width*self.height >= other.width*other.height

class Point:
    """It's a point"""
    def __init__(self, x:int, y:int) -> None:
        self.x:int = int(x)
        self.y:int = int(y)
    
    def __iter__(self):
        yield self.x
        yield self.y

    def rotateAround(self, pivot:Location, angle:float) -> None:
        """Rotates the Point around a pivot Point by a given angle in radians."""
        translated_x = self.x - pivot[0]
        translated_y = self.y - pivot[1]
        
        # Apply the rotation
        rotated_x = translated_x * math.cos(angle) - translated_y * math.sin(angle)
        rotated_y = translated_x * math.sin(angle) + translated_y * math.cos(angle)
        
        # Translate back to the pivot's position
        self.x = rotated_x + pivot[0]
        self.y = rotated_y + pivot[1]
    
    def angleTo(self, other:Location) -> float:
        """Returns the angle to a tuple or Point (x, y)"""
        return math.atan2(other[1] - self.y, other[0] - self.x)
    
    def distanceTo(self, other:Location) -> float:
        """Returns the distance to a tuple or Point (x, y)"""
        return math.sqrt((other[0] - self.x)**2 + (other[1] - self.y)**2)
    
    def toTuple(self) -> tuple:
        """Returns the Point as a tuple (x, y)"""
        return (self.x, self.y)
    
    def move(self, x:int, y:int) -> None:
        self.x += int(x)
        self.y += int(y)

    def moveTowards(self, other:Location, units:float = 1) -> None:
        """Moves the Point towards another Point or tuple (x, y) by 1 unit."""
        angle = self.angleTo(other)
        self.x += int(math.cos(angle)*units)
        self.y += int(math.sin(angle)*units)
    
    def set(self, x:int, y:int) -> None:
        self.x = x
        self.y = y
    
    def __add__(self, other:Vector) -> Point:
        return Point((self.x + other[0]), (self.y + other[1]))
    
    def __sub__(self, other:Vector) -> Point:
        return Point((self.x - other[0]), (self.y - other[1]))
    
    def __mul__(self, other:int|float) -> Point:
        if isinstance(other, Size):
            other = other.width
        return Point((self.x * other), (self.y * other))

    def __truediv__(self, other:int|float) -> Point:
        return Point((self.x / other), (self.y / other))

    def intersectedBy(self, other: Line) -> bool:
        return other.__contains__(self)
    
    def __eq__(self, other:Vector) -> bool:
        return other[0] == self.x and other[1] == self.y
    
    def __contains__(self, other:Point) -> None:
        return other.x == self.x and other.y == self.y
    
    def __getitem__(self, index:int) -> int:
        """Returns the x or y value of the Point
        Honestly, this only exists to make the Point class more like a tuple."""
        if index == 0:
            return self.x
        elif index == 1:
            return self.y
        else:
            raise IndexError("Index out of range for Point. Use 0 for x and 1 for y.")
    
    def limit(self, rect:Rect) -> None:
        """Limits the Point to be within a Rect."""
        self.x = max(rect.x, min(self.x, rect.x + rect.width))
        self.y = max(rect.y, min(self.y, rect.y + rect.height))
    
    def normalize(self) -> Point:
        """Returns a normalized version of the Point as a vector from the origin."""
        length = math.sqrt(self.x**2 + self.y**2)
        if length == 0:
            return Point(0, 0)
        return Point(self.x / length, self.y / length)
    
    def intersectedBy(self, other: Line) -> bool:
        """Checks if the Point is on the Line."""
        return other.__contains__(self)
        
    @dualmethod
    def clone(cls, self:Point) -> Point:
        return Point(self.x, self.y)

    @dualmethod
    def midpoint(cls, self:Point, other:Location) -> Point:
        """Returns the midpoint between two Points."""
        return Point((self.x + other[0])/2, (self.y + other[1])/2)

    @dualmethod
    def collinear(cls, self:Location, foo:Location, bar:Location, accuracy=50) -> bool:
        theta1 = math.atan((foo[1] - self[1])/(foo[0] - self[0]))
        theta2 = math.atan((bar[1] - self[1])/(bar[0] - self[0]))
        return abs(theta1 - theta2) < (1/accuracy)

    def __repr__(self):
        return f"Point({self.x}, {self.y})"
    
    @dualmethod
    def lerp(cls, a:Location, b:Location, t:float) -> Point:
        """Linearly interpolates between two points."""
        return Point(
            a[0] + (b[0] - a[0]) * t, 
            a[1] + (b[1] - a[1]) * t
        )
    
    def __hash__(self):
        return hash((self.x, self.y))

class Line:
    """It's a line"""
    def __init__(self, p1:Point, p2:Point) -> None:
        self.p1:Point = p1
        self.p2:Point = p2

    def __iter__(self):
        yield self.p1
        yield self.p2

    def __len__(self) -> int:
        """Returns the length of the line as an int"""
        return int(math.sqrt((self.p2.x - self.p1.x)**2 + (self.p2.y - self.p1.y)**2))
    
    def length(self) -> float:
        """Returns the length of the line as a float"""
        return math.sqrt((self.p2.x - self.p1.x)**2 + (self.p2.y - self.p1.y)**2)
    
    def clone(self) -> Line:
        """Returns a deep copy of the Line"""
        return Line(self.p1.clone(), self.p2.clone())
    
    def unlink(self) -> None:
        """Unlinks the points from the line, so they can be moved independently."""
        self.p1 = self.p1.clone()
        self.p2 = self.p2.clone()
    
    def midpoint(self) -> Point:
        """Returns the midpoint of the line."""
        return Point((self.p1.x + self.p2.x)/2, (self.p1.y + self.p2.y)/2)

    def slope(self) -> float:
        """Returns the slope of the line."""
        try:
            return (self.p2.y - self.p1.y) / (self.p2.x - self.p1.x)
        except ZeroDivisionError:
            # not infinity (math.inf), but a really big number
            return 1e10
    
    def yIntercept(self) -> float:
        """Returns the y intercept of the line."""
        return self.p1.y - self.slope()*self.p1.x

    def intersection(self, other:Line) -> Point:
        """Returns the intersection point of two lines."""
        # Get positions
        x1, y1 = self.p1.x, self.p1.y
        x2, y2 = self.p2.x, self.p2.y
        x3, y3 = other.p1.x, other.p1.y
        x4, y4 = other.p2.x, other.p2.y

        # Check if the domain and range of the lines overlap using the numbers and not Interval()
        if not (between(x1, x3, x2) or between(x1, x4, x2) or between(x3, x1, x4) or between(x3, x2, x4)):
            return None
        if not (between(y1, y3, y2) or between(y1, y4, y2) or between(y3, y1, y4) or between(y3, y2, y4)):
            return None

        # Get the determinant
        denom = (x1 - x2) * (y3 - y4) - (y1 - y2) * (x3 - x4)
        if denom == 0:
            return None
        
        # Calculate the intersection point
        x = ((x1 * y2 - y1 * x2) * (x3 - x4) - (x1 - x2) * (x3 * y4 - y3 * x4)) / denom
        y = ((x1 * y2 - y1 * x2) * (y3 - y4) - (y1 - y2) * (x3 * y4 - y3 * x4)) / denom
        return Point(x, y)
    
    def intersects(self, other:Line) -> bool:
        """Checks if two lines intersect."""
        return self.intersection(other) is not None
    
    def intersectedBy(self, other:Line) -> bool:
        """Checks if this line is intersected by another line."""
        return self.intersection(other) is not None

    def isParallel(self, other:Line) -> bool:
        """Checks if two lines are parallel."""
        return zero == self.slope() - other.slope()
    
    def isPerpendicular(self, other:Line) -> bool:
        """Checks if two lines are perpendicular."""
        # If the product of the slopes is -1, then they are perpendicular
        return zero == self.slope() - 1 / other.slope()
    
    def isColinear(self, other:Line) -> bool:
        """Checks if two lines are colinear."""
        # If the slopes and y intercepts are the same, then they are colinear
        return zero == self.slope() - other.slope() and zero == self.yIntercept() - other.yIntercept()

    def __contains__(self, p:Point):
        """Checks if a point is colinear"""
        # If the point falls in the domain, then check if the slope and yIntersept work out. Works for error range of (-1, 1)
        return self.slope()*p.x + self.yIntercept() - p.y == zero

    def domain(self) -> Interval:
        """Returns the domain of the line as an Interval."""
        return Interval(self.p1.x, self.p2.x)
    
    def range(self) -> Interval:
        """Returns the range of the line as an Interval."""
        return Interval(self.p1.y, self.p2.y)
    
    def left(self) -> Point:
        """Returns the leftmost point of the line. Not linked."""
        return self.p1 if self.p1.x < self.p2.x else self.p2
    
    def right(self) -> Point:
        """Returns the rightmost point of the line. Not linked."""
        return self.p1 if self.p1.x > self.p2.x else self.p2
    
    def top(self) -> Point:
        """Returns the topmost point of the line. Not linked."""
        return self.p1 if self.p1.y < self.p2.y else self.p2
    
    def bottom(self) -> Point:
        """Returns the bottommost point of the line. Not linked."""
        return self.p1 if self.p1.y > self.p2.y else self.p2
    
    def fint(self) -> tuple[int, int, int, int]:
        """Converts the Line to a tuple of four integers (fint) like (x1, y1, x2, y2) for unpacking or other uses."""
        return (self.p1.x, self.p1.y, self.p2.x, self.p2.y)
    
    def allPoints(self) -> list[Point]:
        """Returns a list of all the points on the line."""
        points = []
        if self.slope() > 1 or self.slope() < -1:
            for y in range(self.p1.y, self.p2.y + 1):
                x = int((y - self.yIntercept()) / self.slope())
                points.append(Point(x, y))
        else:
            for x in range(self.p1.x, self.p2.x + 1):
                y = int(self.slope() * x + self.yIntercept())
                points.append(Point(x, y))
        return points

    def __repr__(self):
        return f"Line({self.p1}, {self.p2})"
    
    def __str__(self):
        return f"Line from {self.p1} to {self.p2}"
    
    def __hash__(self):
        return hash((self.p1.x, self.p1.y, self.p2.x, self.p2.y))

class Ray(Line):
    """A Ray is a line that starts at a point and extends infinitely in one direction."""
    def __init__(self, start:Point, direction:Point|float) -> None:
        if isinstance(direction, float):
            direction = Point(100*math.cos(direction), 100*math.sin(direction))
        super().__init__(start, Point(start.x + direction.x, start.y + direction.y))
    
    @property
    def origin(self) -> Point:
        """Returns the starting point of the Ray."""
        return self.p1

    @origin.setter
    def origin(self, value:Point) -> None:
        """Sets the starting point of the Ray."""
        self.p1 = value
        self.p2 = Point(value.x + (self.p2.x - self.p1.x), value.y + (self.p2.y - self.p1.y))
    
    @property
    def direction(self) -> Point:
        """Returns the direction of the Ray as a Point."""
        return Point(self.p2.x - self.p1.x, self.p2.y - self.p1.y)
    
    @direction.setter
    def direction(self, value:Point) -> None:
        """Sets the direction of the Ray."""
        self.p2 = Point(self.p1.x + value.x, self.p1.y + value.y)

    def __iter__(self):
        """Iterates over the points of the Ray."""
        yield self.p1
        yield self.p2

    def domain(self) -> Interval:
        """Returns the domain of the Ray as an Interval."""
        return Interval(self.p1.x, float('inf')) if self.p2.x >= self.p1.x else Interval(float('-inf'), self.p1.x)
    
    def range(self) -> Interval:
        """Returns the range of the Ray as an Interval."""
        return Interval(self.p1.y, float('inf')) if self.p2.y >= self.p1.y else Interval(float('-inf'), self.p1.y)
    
    def intersection(self, other:Line, distance:float = None) -> Point:
        """Returns the intersection point of two lines. If distance is given, limits the raycast to that distance."""
        # Get positions
        x1, y1 = self.p1.x, self.p1.y
        x2, y2 = self.p2.x, self.p2.y
        x3, y3 = other.p1.x, other.p1.y
        x4, y4 = other.p2.x, other.p2.y

        # Check if the domain and range of the lines overlap using the numbers and not Interval()
        if not self.domain().overlaps(other.domain()) or not self.range().overlaps(other.range()):
            return None

        # Get the determinant
        denom = (x1 - x2) * (y3 - y4) - (y1 - y2) * (x3 - x4)
        if denom == 0:
            return None
        
        # Calculate the intersection point
        x = ((x1 * y2 - y1 * x2) * (x3 - x4) - (x1 - x2) * (x3 * y4 - y3 * x4)) / denom
        y = ((x1 * y2 - y1 * x2) * (y3 - y4) - (y1 - y2) * (x3 * y4 - y3 * x4)) / denom
        intersection_point = Point(x, y)

        if distance is not None:
            # Only allow intersection if within distance from self.p1
            dist = math.sqrt((intersection_point.x - self.p1.x) ** 2 + (intersection_point.y - self.p1.y) ** 2)
            if dist > distance:
                return None

        return intersection_point

    def reverse(self) -> Ray:
        # makes the ray points the opposite direction
        direction = Point(self.p1.x - self.p2.x, self.p1.y - self.p2.y)
        return Ray(self.p1, direction)

    def __str__(self):
        return f"Ray from {self.p1} in the direction of {self.p2}"

class Triangle:
    """Defines a triangular area using three points. Can get things like cetroid and intersections of other."""
    def __init__(self, p1:Location, p2:Location, p3:Location):
        self.p1:Point = p1
        self.p2:Point = p2
        self.p3:Point = p3
    
    def __iter__(self):
        yield self.p1
        yield self.p2
        yield self.p3

    def unlink(self):
        self.p1 = self.p1.clone()
        self.p2 = self.p2.clone()
        self.p3 = self.p3.clone()
    
    def intersectedBy(self, other: Line):
        return other.p1 in self or other.p2 in self or other.intersects(Line(self.p1, self.p2)) or other.intersects(Line(self.p2, self.p3)) or other.intersects(Line(self.p3, self.p1))
    
    def centroid(self) -> Point:
        return Point((self.p1.x + self.p2.x + self.p3.x)/3, (self.p1.y + self.p2.y + self.p3.y)/3)
    
    def contains(self, point:Point) -> bool:
        return (((point.x - self.p2.x) * (self.p1.y - self.p2.y) - (self.p1.x - self.p2.x) * (point.y - self.p2.y)) < 0.0) == (((point.x - self.p3.x) * (self.p2.y - self.p3.y) - (self.p2.x - self.p3.x) * (point.y - self.p3.y)) < 0.0) == (((point.x - self.p1.x) * (self.p3.y - self.p1.y) - (self.p3.x - self.p1.x) * (point.y - self.p1.y)) < 0.0)
    
    def __contains__(self, point:Point) -> bool:
        return (((point.x - self.p2.x) * (self.p1.y - self.p2.y) - (self.p1.x - self.p2.x) * (point.y - self.p2.y)) < 0.0) == (((point.x - self.p3.x) * (self.p2.y - self.p3.y) - (self.p2.x - self.p3.x) * (point.y - self.p3.y)) < 0.0) == (((point.x - self.p1.x) * (self.p3.y - self.p1.y) - (self.p3.x - self.p1.x) * (point.y - self.p1.y)) < 0.0)
    
    def rotate(self, rot:float) -> None:
        cen = self.centroid()
        self.p1.rotateAround(cen, rot)
        self.p2.rotateAround(cen, rot)
        self.p3.rotateAround(cen, rot)
    
    def rotateAround(self, pivot:Point, rot:float):
        self.p1.rotateAround(pivot, rot)
        self.p2.rotateAround(pivot, rot)
        self.p3.rotateAround(pivot, rot)
    
    def area(self) -> float:
        """Returns the area of the triangle using Heron's formula"""
        a = math.sqrt((self.p1.x - self.p2.x)**2 + (self.p1.y - self.p2.y)**2)
        b = math.sqrt((self.p2.x - self.p3.x)**2 + (self.p2.y - self.p3.y)**2)
        c = math.sqrt((self.p3.x - self.p1.x)**2 + (self.p3.y - self.p1.y)**2)
        s = (a + b + c) / 2
        return math.sqrt(s * (s - a) * (s - b) * (s - c))
    
    def perimeter(self) -> float:
        """Returns the perimeter of the triangle"""
        a = math.sqrt((self.p1.x - self.p2.x)**2 + (self.p1.y - self.p2.y)**2)
        b = math.sqrt((self.p2.x - self.p3.x)**2 + (self.p2.y - self.p3.y)**2)
        c = math.sqrt((self.p3.x - self.p1.x)**2 + (self.p3.y - self.p1.y)**2)
        return a + b + c
    
    def clone(self) -> Triangle:
        """Returns a deep copy of the Triangle"""
        return Triangle(self.p1.clone(), self.p2.clone(), self.p3.clone())

    def become(self, other:Triangle) -> None:
        """Makes this Triangle the same as another Triangle"""
        self.p1.x = other.p1.x
        self.p1.y = other.p1.y
        self.p2.x = other.p2.x
        self.p2.y = other.p2.y
        self.p3.x = other.p3.x
        self.p3.y = other.p3.y

    def move(self,x:int,y:int):
        self.p1.move(x,y)
        self.p2.move(x,y)
        self.p3.move(x,y)

    @property
    def pos(self) -> Point:
        """Returns the position of the Triangle as a Point"""
        return self.centroid()
    
    @pos.setter
    def pos(self, value:Point) -> None:
        """Sets the position of the Triangle to a Point"""
        dx = value.x - self.centroid().x
        dy = value.y - self.centroid().y
        self.p1.move(dx, dy)
        self.p2.move(dx, dy)
        self.p3.move(dx, dy)

    def __repr__(self):
        return f"Triangle({self.p1}, {self.p2}, {self.p3})"
    
    def __str__(self):
        return f"Triangle with points {self.p1}, {self.p2}, {self.p3}"
    
    def __add__(self, other:Location) -> Triangle:
        """Adds a Point to the Triangle, moving all points by that amount."""
        return Triangle(self.p1 + other, self.p2 + other, self.p3 + other)
    
    def __sub__(self, other:Location) -> Triangle:
        """Subtracts a Point from the Triangle, moving all points by that amount."""
        return Triangle(self.p1 - other, self.p2 - other, self.p3 - other)

class Quad:
    """Defines a quadrilateral area using four points. Can get things like cetroid and intersections of other."""
    def __init__(self, p1:Location, p2:Location, p3:Location, p4:Location):
        self.p1:Point = p1
        self.p2:Point = p2
        self.p3:Point = p3
        self.p4:Point = p4
    
    def __iter__(self):
        yield self.p1
        yield self.p2
        yield self.p3
        yield self.p4

    def unlink(self):
        self.p1 = self.p1.clone()
        self.p2 = self.p2.clone()
        self.p3 = self.p3.clone()
        self.p4 = self.p4.clone()
    
    def intersectedBy(self, other: Line):
        return other.p1 in self or other.p2 in self or other.intersects(Line(self.p1, self.p2)) or other.intersects(Line(self.p2, self.p3)) or other.intersects(Line(self.p3, self.p4)) or other.intersects(Line(self.p4, self.p1))
    
    def centroid(self) -> Point:
        return Point((self.p1.x + self.p2.x + self.p3.x + self.p4.x)/4, (self.p1.y + self.p2.y + self.p3.y + self.p4.y)/4)
    
    def contains(self, point:Point) -> bool:
        # Returns if the point is inside the quadrilateral using the cross product method
        return (((point.x - self.p2.x) * (self.p1.y - self.p2.y) - (self.p1.x - self.p2.x) * (point.y - self.p2.y)) < 0.0) == (((point.x - self.p3.x) * (self.p2.y - self.p3.y) - (self.p2.x - self.p3.x) * (point.y - self.p3.y)) < 0.0) == (((point.x - self.p4.x) * (self.p3.y - self.p4.y) - (self.p3.x - self.p4.x) * (point.y - self.p4.y)) < 0.0) == (((point.x - self.p1.x) * (self.p4.y - self.p1.y) - (self.p4.x - self.p1.x) * (point.y - self.p1.y)) < 0.0)

    def __contains__(self, point:Point) -> bool:
        return self.contains(point)
    
    def rotate(self, rot:float) -> None:
        cen = self.centroid()
        self.p1.rotateAround(cen, rot)
        self.p2.rotateAround(cen, rot)
        self.p3.rotateAround(cen, rot)
        self.p4.rotateAround(cen, rot)
    
    def __add__(self, other:Location) -> Quad:
        """Adds a Point to the Quad, moving all points by that amount."""
        return Quad(self.p1 + other, self.p2 + other, self.p3 + other, self.p4 + other)
    
    def __sub__(self, other:Location) -> Quad:
        """Subtracts a Point from the Quad, moving all points by that amount."""
        return Quad(self.p1 - other, self.p2 - other, self.p3 - other, self.p4 - other)
    
    def area(self) -> float:
        """Returns the area of the quadrilateral using the shoelace formula"""
        return abs((self.p1.x * self.p2.y + self.p2.x * self.p3.y + self.p3.x * self.p4.y + self.p4.x * self.p1.y) - (self.p2.x * self.p1.y + self.p3.x * self.p2.y + self.p4.x * self.p3.y + self.p1.x * self.p4.y)) / 2

class Rect:
    """Define a rectangular area using an x and y from the top left along with the height and width. Methods inside allow you to check if points, lines, or other Rects pass through it, and it can be easily drawn"""
    def __init__(self, position:Point, dimensions:Size) -> None:
        self.pos:Point = position
        self.size:Size = dimensions
    
    def __iter__(self):
        yield self.pos
        yield self.size
    
    def fint(self) -> tuple[int, int, int, int]:
        """Converts the Rect to a tuple of four integers (fint) like (x, y, width, height) for unpacking or other uses."""
        return (self.pos.x, self.pos.y, self.size.width, self.size.height)

    def contains(self, x:int | Vector, y:int = None) -> bool:
        """Returns if the inputted point is in the area, takes an x and y, a tuple, list, or Point()"""
        if isinstance(x, Vector):
            return x[0] > self.pos.x and x[1] > self.pos.y and x[1] < self.pos.y + self.size.height and x[0] < self.pos.x + self.size.width
        return x > self.pos.x and y > self.pos.y and y < self.pos.y + self.size.height and x < self.pos.x + self.size.width
    
    def __contains__(self, point:Location) -> bool:
        return point[0] > self.pos.x and point[1] > self.pos.y and point[1] < self.pos.y + self.size.height and point[0] < self.pos.x + self.size.width
    
    @property
    def center(self) -> Point:
        """Returns the center of the Rect, not linked"""
        return Point(self.pos.x + self.size.width/2, self.pos.y + self.size.height/2)
    
    @center.setter
    def center(self, value:Location) -> None:
        """Sets the center of the Rect to a Point"""
        self.pos.x += value[0] - self.center.x
        self.pos.y += value[1] - self.center.y
    
    def perimeter(self) -> float:
        """Returns the perimeter of the Rect"""
        return 2 * (self.size.width + self.size.height)

    def perimeterPoint(self, rotation:float) -> Point:
        """
        Returns a Point on the perimeter of the Rect at a given traced amount from 0 to 1
        rotation is a float from 0 to 1, where it will trace fully around at 1.
        So on a perfect square, 0.25 would be the top right corner, 0.5 would be the bottom right corner, and so on.
        If the rotation is greater than 1, it will wrap around.
        If the rotation is less than 0, it will wrap around in the opposite direction.
        """

        perimeter = self.perimeter()
        pos = (rotation % 1) * perimeter
        
        if pos < self.size.width: 
            return Point(self.pos.x + pos, self.pos.y)
        pos -= self.size.width
        
        if pos < self.size.height:
            return Point(self.pos.x + self.size.width, self.pos.y + pos)
        pos -= self.size.height
        
        if pos < self.size.width:
            return Point(self.pos.x + self.size.width - pos, self.pos.y + self.size.height)
        pos -= self.size.width
        
        return Point(self.pos.x, self.pos.y + self.size.height - pos)

    def corners(self) -> tuple[Point, Point, Point, Point]:
        """Returns the four corners of the Rect as Points"""
        TR = Point(self.pos.x, self.pos.y)
        TL = Point(self.pos.x + self.size.width, self.pos.y)
        BR = Point(self.pos.x, self.pos.y + self.size.height)
        BL = Point(self.pos.x + self.size.width, self.pos.y + self.size.height)
        return (TR, TL, BR, BL)

    def edges(self) -> tuple[Line, Line, Line, Line]:
        """Returns a tuple of the 4 edges of the Rect, NOT LINKED"""
        TR, TL, BR, BL = self.corners()
        return (Line(TL, TR), Line(TL, BL), Line(BL, BR), Line(TR, BR))

    def intersectedBy(self, line: Line) -> bool:
        """Returns if a line intersects with the Rect"""
        TR = Point(self.pos.x, self.pos.y)
        TL = Point(self.pos.x + self.size.width, self.pos.y)
        BR = Point(self.pos.x, self.pos.y + self.size.height)
        BL = Point(self.pos.x + self.size.width, self.pos.y + self.size.height)
        if line.length() == 0:
            return self.contains(line.p1)
        return self.contains(line.p1) or self.contains(line.p2) or line.intersectedBy(Line(TR, TL)) or line.intersectedBy(Line(BR, BL)) or line.intersectedBy(Line(TR, BR)) or line.intersectedBy(Line(TL, BL))
    
    def clone(self) -> Rect:
        """Returns a deep copy of the Rect"""
        return Rect(self.pos.clone(), self.size.clone())

    def overlaps(self, other: Rect) -> bool:
        """Returns if another Rect overlaps with it"""
        return self.pos.x < other.pos.x + other.size.width and self.pos.x + self.size.width > other.pos.x and self.pos.y < other.pos.y + other.size.height and self.pos.y + self.size.height > other.pos.y
    
    def move(self, x:int, y:int):
        """Moves the Rect by (x, y)"""
        self.pos.x += x
        self.pos.y += y

    def become(self, other:Rect) -> None:
        """Makes this Rect the same as another Rect"""
        self.pos.x = other.pos.x
        self.pos.y = other.pos.y
        self.size.width = other.size.width
        self.size.height = other.size.height

    @property
    def x(self) -> int:
        """Returns the x position of the Rect"""
        return self.pos.x
    
    @property
    def y(self) -> int:
        """Returns the y position of the Rect"""
        return self.pos.y
    
    @property
    def width(self) -> int:
        """Returns the width of the Rect"""
        return self.size.width
    
    @property
    def height(self) -> int:
        """Returns the height of the Rect"""
        return self.size.height
    
    @x.setter
    def x(self, value:int) -> None:
        """Sets the x position of the Rect"""
        self.pos.x = value

    @y.setter
    def y(self, value:int) -> None:
        """Sets the y position of the Rect"""
        self.pos.y = value

    @width.setter
    def width(self, value:int) -> None:
        """Sets the width of the Rect"""
        self.size.width = value

    @height.setter
    def height(self, value:int) -> None:
        """Sets the height of the Rect"""
        self.size.height = value

    def __repr__(self):
        return f"Rect({self.pos}, {self.size})"
    
    def __str__(self):
        return f"Rect at {self.pos} with size {self.size}"
    
    def __add__(self, other:Vector) -> Rect:
        """Adds a Point or Size from the Rect, moving or scaling the rect by that amount."""
        if isinstance(other, Point):
            return Rect(Point(self.pos.x + other.x, self.pos.y + other.y), self.size)
        elif isinstance(other, Size):
            return Rect(self.pos, Size(self.size.width + other.width, self.size.height + other.height))
        elif isinstance(other, tuple):
            return Rect(Point(self.pos.x + other[0], self.pos.y + other[1]), self.size)
        else:
            raise TypeError("Unsupported type for addition with Rect")
    
    def __sub__(self, other:Vector) -> Rect:
        """Subtracts a Point or Size from the Rect, moving or scaling the rect by that amount."""
        if isinstance(other, Point):
            return Rect(Point(self.pos.x - other.x, self.pos.y - other.y), self.size)
        elif isinstance(other, Size):
            return Rect(self.pos, Size(self.size.width - other.width, self.size.height - other.height))
        elif isinstance(other, tuple):
            return Rect(Point(self.pos.x - other[0], self.pos.y - other[1]), self.size)
        else:
            raise TypeError("Unsupported type for subtraction with Rect")
    
    def __mul__(self, other:Number) -> Rect:
        """Multiplies the size of the Rect by a scalar."""
        if isinstance(other, (int, float)):
            return Rect(self.pos, Size(int(self.size.width * other), int(self.size.height * other)))
        else:
            raise TypeError("Unsupported type for multiplication with Rect")

class Ellipse:
    """An Ellipse is defined by a center Point and a Size"""
    def __init__(self, center:Point, size:Size) -> None:
        self.pos:Point = center
        self.size:Size = size
    
    def __iter__(self):
        yield self.pos
        yield self.size
    
    def intersectedBy(self, line: Line) -> bool:
        ax = (line.p1.x - self.pos.x) / self.size.width
        ay = (line.p1.y - self.pos.y) / self.size.height
        bx = (line.p2.x - self.pos.x) / self.size.width
        by = (line.p2.y - self.pos.y) / self.size.height

        # Direction vector
        dx = bx - ax
        dy = by - ay

        # Vector from center to point A (in normalized space)
        fx = ax
        fy = ay

        # Coefficients for the quadratic
        a = dx*dx + dy*dy
        b = 2 * (fx*dx + fy*dy)
        c = fx*fx + fy*fy - 1  # Unit circle, so r^2 = 1

        discriminant = b*b - 4*a*c

        if discriminant < 0:
            return False  # No intersection
        else:
            # Checks if the intersection points are within the line segment
            discriminant = math.sqrt(discriminant)
            return (0 <= ((-b - discriminant) / (2*a)) <= 1) or (0 <= ((-b + discriminant) / (2*a)) <= 1)

    def __repr__(self):
        return f"Ellipse({self.pos}, {self.size})"
    
    def __str__(self):
        return f"Ellipse at {self.pos} with size {self.size}"
    
    def area(self) -> float:
        """Returns the area of the Ellipse"""
        return math.pi * (self.size.width/2) * (self.size.height/2)
    
    def perimeter(self) -> float:
        """Returns the perimeter of the Ellipse"""
        a = self.size.width/2
        b = self.size.height/2
        return math.pi * (3*(a + b) - math.sqrt((3*a + b)*(a + 3*b)))
    
    def clone(self) -> Ellipse:
        """Returns a deep copy of the Ellipse"""
        return Ellipse(self.pos.clone(), self.size.clone())
    
    def __contains__(self, point:Location) -> bool:
        """Returns if a point is inside the Ellipse"""
        px = (point[0] - self.pos.x) / (self.size.width / 2)
        py = (point[1] - self.pos.y) / (self.size.height / 2)
        return px*px + py*py <= 1

    @property
    def center(self) -> Point:
        """Returns the center of the Ellipse as a Point"""
        return self.pos
    
    @center.setter
    def center(self, value:Location) -> None:
        """Sets the center of the Ellipse to a Point. The inputed Point will not be linked."""
        self.pos.x = value[0]
        self.pos.y = value[1]

class Circle(Ellipse):
    """An Circle is defined by a center Point and a radius"""
    def __init__(self, center:Point, radius:int) -> None:
        super().__init__(center, Size(radius*2, radius*2))
    
    def area(self) -> float:
        """Returns the area of the Circle"""
        return math.pi * (self.size.width/2)**2
    
    def perimeter(self) -> float:
        """Returns the perimeter of the Circle"""
        return 2 * math.pi * (self.size.width/2)
    
    @property
    def radius(self) -> int:
        """Returns the radius of the Circle"""
        return self.size.width/2

    @radius.setter
    def radius(self, radius:int) -> None:
        """Sets the radius of the Circle"""
        self.size.width = radius*2
        self.size.height = radius*2

def touches(a:Shape, b:Shape) -> bool:
    """Returns if two shapes touch each other."""
    if isinstance(a, Line):
        return b.intersectedBy(a)
    elif isinstance(b, Line):
        return a.intersectedBy(b)
    if isinstance(a, Point):
        return a in b
    elif isinstance(b, Point):
        return b in a
    elif isinstance(a, Rect) and isinstance(b, Rect):
        return a.overlaps(b)
    elif isinstance(a, Ellipse) and isinstance(b, Ellipse):
        # Check if the distance between the centers is less than the sum of the radii
        dx = a.pos.x - b.pos.x
        dy = a.pos.y - b.pos.y
        distance = math.sqrt(dx*dx + dy*dy)
        return distance < (a.size.width/2 + b.size.width/2) and distance < (a.size.height/2 + b.size.height/2)
    elif isinstance(a, Rect) and isinstance(b, Ellipse):
        # Find the closest point on the rectangle to the center of the ellipse
        closestX = max(a.pos.x, min(b.pos.x, a.pos.x + a.size.width))
        closestY = max(a.pos.y, min(b.pos.y, a.pos.y + a.size.height))

        # Calculate the distance between the ellipse's center and this closest point
        dx = b.pos.x - closestX
        dy = b.pos.y - closestY

        # If the distance is less than the radius, they are touching
        return (dx*dx + dy*dy) < (b.size.width/2)**2 and (dx*dx + dy*dy) < (b.size.height/2)**2
    elif isinstance(a, Ellipse) and isinstance(b, Rect):
        return touches(b, a)
    elif isinstance(a, Triangle) and isinstance(b, Triangle):
        return a.contains(b.p1) or a.contains(b.p2) or a.contains(b.p3) or b.contains(a.p1) or b.contains(a.p2) or b.contains(a.p3) or a.intersectedBy(Line(b.p1, b.p2)) or a.intersectedBy(Line(b.p2, b.p3)) or a.intersectedBy(Line(b.p3, b.p1)) or b.intersectedBy(Line(a.p1, a.p2)) or b.intersectedBy(Line(a.p2, a.p3)) or b.intersectedBy(Line(a.p3, a.p1))
    elif isinstance(a, Triangle) and isinstance(b, Rect):
        return a.contains(b.pos) or a.contains(Point(b.pos.x + b.size.width, b.pos.y)) or a.contains(Point(b.pos.x, b.pos.y + b.size.height)) or a.contains(Point(b.pos.x + b.size.width, b.pos.y + b.size.height)) or b.contains(a.p1) or b.contains(a.p2) or b.contains(a.p3) or a.intersectedBy(Line(b.pos, Point(b.pos.x + b.size.width, b.pos.y))) or a.intersectedBy(Line(Point(b.pos.x + b.size.width, b.pos.y), Point(b.pos.x + b.size.width, b.pos.y + b.size.height))) or a.intersectedBy(Line(Point(b.pos.x + b.size.width, b.pos.y + b.size.height), Point(b.pos.x, b.pos.y + b.size.height))) or a.intersectedBy(Line(Point(b.pos.x, b.pos.y + b.size.height), b.pos))
    elif isinstance(a, Rect) and isinstance(b, Triangle):
        return touches(b, a)
    elif isinstance(a, Quad) and isinstance(b, Quad):
        return a.contains(b.p1) or a.contains(b.p2) or a.contains(b.p3) or a.contains(b.p4) or b.contains(a.p1) or b.contains(a.p2) or b.contains(a.p3) or b.contains(a.p4) or a.intersectedBy(Line(b.p1, b.p2)) or a.intersectedBy(Line(b.p2, b.p3)) or a.intersectedBy(Line(b.p3, b.p4)) or a.intersectedBy(Line(b.p4, b.p1)) or b.intersectedBy(Line(a.p1, a.p2)) or b.intersectedBy(Line(a.p2, a.p3)) or b.intersectedBy(Line(a.p3, a.p4)) or b.intersectedBy(Line(a.p4, a.p1))
    elif isinstance(a, Quad) and isinstance(b, Rect):
        return a.contains(b.pos) or a.contains(Point(b.pos.x + b.size.width, b.pos.y)) or a.contains(Point(b.pos.x, b.pos.y + b.size.height)) or a.contains(Point(b.pos.x + b.size.width, b.pos.y + b.size.height)) or b.contains(a.p1) or b.contains(a.p2) or b.contains(a.p3) or b.contains(a.p4) or a.intersectedBy(Line(b.pos, Point(b.pos.x + b.size.width, b.pos.y))) or a.intersectedBy(Line(Point(b.pos.x + b.size.width, b.pos.y), Point(b.pos.x + b.size.width, b.pos.y + b.size.height))) or a.intersectedBy(Line(Point(b.pos.x + b.size.width, b.pos.y + b.size.height), Point(b.pos.x, b.pos.y + b.size.height))) or a.intersectedBy(Line(Point(b.pos.x, b.pos.y + b.size.height), b.pos))
    elif isinstance(a, Rect) and isinstance(b, Quad):
        return touches(b, a)
    else:
        raise TypeError("Unsupported shape types for touches(Shape, Shape)")
    
class ShapeForm:
    """A ShapeForm is a collection of shapes that can be drawn together."""
    def __init__(self, shapes:Form) -> None:
        if isinstance(shapes, list):
            self.shapes:list[Shape] = shapes
        elif isinstance(shapes, ShapeForm):
            self.shapes:list[Shape] = shapes.shapes.copy()
        else:
            self.shapes:list[Shape] = [shapes]
    
    def add(self, shape:Shape) -> None:
        """Adds a shape to the ShapeForm."""
        self.shapes.append(shape)
    
    def remove(self, shape:Shape) -> None:
        """Removes a shape from the ShapeForm."""
        self.shapes.remove(shape)
    
    def clear(self) -> None:
        """Clears all shapes from the ShapeForm."""
        self.shapes.clear()
    
    def clone(self) -> ShapeForm:
        """Returns a deep copy of the ShapeForm."""
        return ShapeForm([shape.clone() for shape in self.shapes])
    
    def intersectedBy(self, line: Line) -> bool:
        """Returns if a line intersects with any shape in the ShapeForm."""
        return any(shape.intersectedBy(line) for shape in self.shapes if hasattr(shape, 'intersectedBy'))
    
    def touches(self, other:Form) -> bool:
        """Returns if this ShapeForm touches another shape or shape form."""
        if isinstance(other, Shape):
            return any(touches(shape, other) for shape in self.shapes)
        elif isinstance(other, ShapeForm):
            return any(touches(shape, other_shape) for shape in self.shapes for other_shape in other.shapes)
        elif isinstance(other, list):
            return any(touches(shape, other_shape) for shape in self.shapes for other_shape in other)
        return False

    def __iter__(self):
        yield from self.shapes
    
    def __repr__(self):
        return f"ShapeForm({self.shapes})"
    
    def __str__(self):
        return f"ShapeForm with {len(self.shapes)} shapes"

def isinstances(args:tuple, types:tuple[type]) -> bool:
    """Checks if all arguments are instances of the given types."""
    return len(args) == len(types) and all(isinstance(arg, typ) for arg, typ in zip(args, types))

# 5 important unions
Number = Union[int, float]
Shape = Union[Point, Line, Ray, Triangle, Quad, Rect, Ellipse, Circle]
Location = Union[Point, tuple]
Vector = Union[Point, Size, tuple]
Form = Union[Shape, ShapeForm, list]

def I(*args) -> Interval:
    """A more broad Interval constructor."""
    if len(args) == 1 and isinstance(args[0], tuple):
        if len(args[0]) != 2:
            raise Exception(f"Invalid tuple length for I: {args[0]}")
        return Interval(*args[0])
    elif len(args) == 1 and isinstance(args[0], Interval):
        return args[0].clone()
    elif len(args) == 2:
        return Interval(*args)
    else:
        raise Exception(f"Invalid arguments for I: {args}")

Sizeable = Union[tuple[Number, Number], Size, Point, Line]
def S(*args: Sizeable) -> Size:
    """A more broad Size constructor."""
    if len(args) == 1 and isinstance(args[0], tuple): # tuple -> ([0], [1])
        if len(args[0]) != 2:
            raise Exception(f"Invalid tuple length for S: {args[0]}")
        return Size(*args[0])
    elif len(args) == 1 and isinstance(args[0], Size): # Size -> (width, height)
        return args[0].clone()
    elif len(args) == 1 and isinstance(args[0], Point): # Point -> (x, y)
        return Size(args[0].x, args[0].y)
    elif len(args) == 1 and isinstance(args[0], Line): # Line -> (dx, dy)
        return Size(abs(args[0].p2.x - args[0].p1.x), abs(args[0].p2.y - args[0].p1.y))
    elif len(args) == 2: # Numbers -> (Number 1, Number 2)
        return Size(*args)
    else:
        raise Exception(f"Invalid arguments for S: {args}")

Pointable = Union[tuple[Number, Number], tuple[Vector]]
def P(*args: Pointable) -> Point:
    """A more broad Point constructor."""
    if len(args) == 1 and isinstance(args[0], Vector): # tuple, point, size, pair -> (x, y)
        return Point(*args[0])
    elif len(args) == 2: # Numbers -> (Number 1, Number 2)
        return Point(*args)
    else:
        raise Exception(f"Invalid arguments for P: {args}")

Lineable = Union[tuple[Number, Number, Number, Number], tuple[tuple[Number, Number], tuple[Number, Number]], tuple[Point, Point], Line]
def L(*args: Lineable) -> Line:
    """A more broad Line constructor. Points are linked."""
    if len(args) == 2 and isinstance(args[0], tuple):
        if len(args[0]) != 2:
            raise Exception(f"Invalid tuple length for P: {args[0]}")
        return Line(Point(*args[0]), Point(*args[1]))
    elif len(args) == 2 and isinstance(args[0], Point): 
        return Line(args[0], args[1])
    elif len(args) == 1 and isinstance(args[0], Line):
        return args[0].clone()
    elif len(args) == 2:
        return Line(*args)
    else:
        raise Exception(f"Invalid arguments for L: {args}")

Triangleable = Union[tuple[Number, Number, Number, Number, Number, Number], tuple[tuple[Number, Number], tuple[Number, Number], tuple[Number, Number]], tuple[Point, Point, Point], Size, Triangle]
def T(*args: Triangleable) -> Triangle:
    """A more broad Triangle constructor. Points are linked."""
    if len(args) == 6 and isinstance(args[0], Number):
        return Triangle(Point(args[0], args[1]), Point(args[2], args[3]), Point(args[4], args[5]))
    elif len(args) == 3 and isinstance(args[0], tuple):
        if len(args[0]) != 2:
            raise Exception(f"Invalid tuple length for T: {args[0]}")
        return Triangle(Point(*args[0]), Point(*args[1]), Point(*args[2]))
    elif isinstances(args, (Point, Point, Point)): # Points
        return Triangle(args[0], args[1], args[2])
    elif isinstances(args, (Point, Number)): # Position and radius
        return Triangle(Point(args[0].x + math.cos(2*math.pi/3) * args[1], args[0].y + math.sin(2*math.pi/3) * args[1]), Point(args[0].x + math.cos(4*math.pi/3) * args[1], args[0].y + math.sin(4*math.pi/3) * args[1]), Point(args[0].x + math.cos(0) * args[1], args[0].y + math.sin(0) * args[1]))
    elif isinstances(args, (tuple, Number)): # Position and radius
        return Triangle(Point(args[0][0] + math.cos(2*math.pi/3) * args[1], args[0][1] + math.sin(2*math.pi/3) * args[1]), Point(args[0][0] + math.cos(4*math.pi/3) * args[1], args[0][1] + math.sin(4*math.pi/3) * args[1]), Point(args[0][0] + math.cos(0) * args[1], args[0][1] + math.sin(0) * args[1]))
    elif len(args) == 1 and isinstance(args[0], Number): # radius
        return Triangle(Point(args[0], 0), Point(math.cos(2*math.pi/3) * args[0], math.sin(2*math.pi/3) * args[0]), Point(math.cos(4*math.pi/3) * args[0], math.sin(4*math.pi/3) * args[0]))
    elif len(args) == 1 and isinstance(args[0], Triangle):
        return args[0].clone()
    elif len(args) == 1 and isinstance(args[0], Size):
        tri = T(1)
        for p in [tri.p1, tri.p2, tri.p3]:
            p.x *= args[0].width
            p.y *= args[0].height
        return tri
    else:
        raise Exception(f"Invalid arguments for T: {args}")

Quadable = Union[tuple[Number, Number, Number, Number, Number, Number, Number, Number], tuple[tuple[Number, Number], tuple[Number, Number], tuple[Number, Number], tuple[Number, Number]], tuple[Point, Point, Point, Point], Quad]
def Q(*args: Quadable) -> Quad:
    """A more broad Quad constructor. Points are linked."""
    if isinstances(args, (Number, Number, Number, Number, Number, Number, Number, Number)): # numbers -> (x1, y1, x2, y2, x3, y3, x4, y4)
        return Quad(Point(args[0], args[1]), Point(args[2], args[3]), Point(args[4], args[5]), Point(args[6], args[7]))
    elif isinstances(args, (tuple, tuple, tuple, tuple)): # tuples -> ((x1, y1), (x2, y2), (x3, y3), (x4, y4))
        if len(args[0]) != 2:
            raise Exception(f"Invalid tuple length for Q: {args[0]}")
        return Quad(Point(*args[0]), Point(*args[1]), Point(*args[2]), Point(*args[3]))
    elif isinstances(args, (Point, Point, Point, Point)): # Points
        return Quad(args[0], args[1], args[2], args[3])
    elif isinstances(args, (Quad,)): # Quad
        return args[0].clone()
    else:
        raise Exception(f"Invalid arguments for Q: {args}")

Rectable = Union[tuple[Number, Number, Number, Number], tuple[tuple[Number, Number], tuple[Number, Number]], tuple[Point, Size], tuple[Rect], tuple[Point, Point], tuple[Point, Number, Number], tuple[Number, Number, Number], tuple[Point, Number]]
def R(*args: Rectable) -> Rect:
    """
    A more broad Rect constructor. Points are linked.

    Accepted argument patterns:
    - R(x, y, w, h)      : Number, Number, Number, Number
    - R((x, y), (w, h))  : tuple[Number, Number], tuple[Number, Number]
    - R(Point, Size)     : Point, Size
    - R(Rect)            : Rect
    - R(Point, Point)    : Point, Point
    - R(Point, w, h)     : Point, Number, Number
    - R(x, y, size)      : Number, Number, Number
    - R(Point, size)     : Point, Number
    """
    # replace all floats with ints
    args = [int(arg) if isinstance(arg, float) else arg for arg in args]

    # If R(x,y,w,h)
    if len(args) == 4 and isinstance(args[0], Number):
        return Rect(Point(args[0], args[1]), Size(args[2], args[3]))
    # If R((x,y),(w,h))
    elif len(args) == 2 and isinstance(args[0], tuple):
        if len(args[0]) != 2:
            raise Exception(f"Invalid tuple length for R: {args[0]}")
        return Rect(Point(*args[0]), Size(*args[1]))
    # If R(Point, Size)
    elif len(args) == 2 and isinstance(args[0], Point) and isinstance(args[1], Size):
        return Rect(args[0], args[1])
    # If R(Rect)
    elif len(args) == 1 and isinstance(args[0], Rect):
        return args[0].clone()
    # If R(Point, Point) makes them the two corners
    elif len(args) == 2 and isinstance(args[0], Point) and isinstance(args[1], Point):
        return Rect(Point(min(args[0].x, args[1].x), min(args[0].y, args[1].y)), Size(abs(args[0].x - args[1].x), abs(args[0].y - args[1].y)))
    # If R(Point, w, h)
    elif len(args) == 3 and isinstance(args[0], Point) and isinstance(args[1], Number) and isinstance(args[2], Number):
        return Rect(args[0], Size(args[1], args[2]))
    # If R(x,y,size:Number) makes a square
    elif len(args) == 3 and isinstance(args[0], Number) and isinstance(args[1], Number) and isinstance(args[2], Number):
        return Rect(Point(args[0], args[1]), Size(args[2], args[2]))
    # if R(Point, size:Number)
    elif len(args) == 2 and isinstance(args[0], Point) and isinstance(args[1], Number):
        return Rect(args[0], Size(args[1], args[1]))
    else:
        raise Exception(f"Invalid arguments for R: {args}")

Ellipseable = Union[tuple[Number, Number, Number, Number], tuple[tuple[Number, Number], tuple[Number, Number]], tuple[Point, Size], tuple[Ellipse], tuple[Point, Point], tuple[Point, Number, Number], tuple[Number, Number, Number], tuple[Point, Number]]
def E(*args: Ellipseable) -> Ellipse:
    """A more broad Ellipse constructor. Points are linked."""
    # If E(x,y,w,h)
    if len(args) == 4 and isinstance(args[0], Number):
        return Ellipse(Point(args[0], args[1]), Size(args[2], args[3]))
    # If E((x,y),(w,h))
    elif len(args) == 2 and isinstance(args[0], tuple):
        if len(args[0]) != 2:
            raise Exception(f"Invalid tuple length for E: {args[0]}")
        return Ellipse(Point(*args[0]), Size(*args[1]))
    # If E(Point, Size)
    elif len(args) == 2 and isinstance(args[0], Point) and isinstance(args[1], Size):
        return Ellipse(args[0], args[1])
    # If E(Ellipse)
    elif len(args) == 1 and isinstance(args[0], Ellipse):
        return args[0].clone()
    # If E(Point, Point) makes them the two corners
    elif len(args) == 2 and isinstance(args[0], Point) and isinstance(args[1], Point):
        return Ellipse(Point(min(args[0].x, args[1].x), min(args[0].y, args[1].y)), Size(abs(args[0].x - args[1].x), abs(args[0].y - args[1].y)))
    # If E(Point, w, h)
    elif len(args) == 3 and isinstance(args[0], Point) and isinstance(args[1], Number) and isinstance(args[2], Number):
        return Ellipse(args[0], Size(args[1], args[2]))
    # If E(x,y,size:Number) makes a circle
    elif len(args) == 3 and isinstance(args[0], Number) and isinstance(args[1], Number) and isinstance(args[2], Number):
        return Ellipse(Point(args[0], args[1]), Size(args[2], args[2]))
    # if E(Point, size:Number) makes a circle
    elif len(args) == 2 and isinstance(args[0], Point) and isinstance(args[1], Number):
        return Ellipse(args[0], Size(args[1], args[1]))
    else:
        raise Exception(f"Invalid arguments for E: {args}")

Circleable = Union[tuple[Number, Number, Number], tuple[tuple[Number, Number], Number], tuple[Point, Number], tuple[Circle]]
def C(*args: Circleable) -> Circle:
    """A more broad Circle constructor. Points are linked."""
    # If C(x,y,radius)
    if len(args) == 3 and isinstance(args[0], Number):
        return Circle(Point(args[0], args[1]), args[2])
    # If C((x,y),radius)
    elif len(args) == 2 and isinstance(args[0], tuple):
        if len(args[0]) != 2:
            raise Exception(f"Invalid tuple length for C: {args[0]}")
        return Circle(Point(*args[0]), args[1])
    # If C(Point, radius)
    elif len(args) == 2 and isinstance(args[0], Point) and isinstance(args[1], Number):
        return Circle(args[0], args[1])
    # If C(Circle)
    elif len(args) == 1 and isinstance(args[0], Circle):
        return args[0].clone()
    else:
        raise Exception(f"Invalid arguments for C: {args}")

