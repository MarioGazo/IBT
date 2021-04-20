from random import choice, randrange, uniform
from string import ascii_uppercase
from Enums import Ways, ElementTypes


class Element:
    """
    Class representing picture element, it's moved by the two-dimensional finite automata
    """
    x, y = 0, 0
    elem_type = None

    def __init__(self, base, x: int, y: int, elem_type: ElementTypes):
        """
        Element class constructor
        :param base: Base to draw into
        :param x: Element x coordinate
        :param y: Element y coordinate
        :param elem_type: Type of the element
        """
        self.x, self.y = x, y
        self.w, self.h = base.cell_w, base.cell_h
        self.elem_type = elem_type
        self.canvas = base.canvas
        self.RAND = 0 if base.DEBUG else 1

        size = round(min(self.w, self.h))
        if elem_type == ElementTypes.DEBUG:
            self.symbol = "#"
            self.id = base.canvas.create_text(x*self.w + self.w/2, y*self.h + self.h/2,
                                              font="Times "+str(size)+" italic", text=self.symbol)
            return

        if elem_type == ElementTypes.LETTER:
            self.symbol = choice(ascii_uppercase)
        elif elem_type == ElementTypes.NUMBER:
            self.symbol = randrange(10)
        coord_x = x*self.w + self.w/2 + self.w/4*uniform(-1, 1)*self.RAND
        coord_y = y*self.h + self.h/2 + self.h/4*uniform(-1, 1)*self.RAND
        self.id = base.canvas.create_text(coord_x, coord_y, font="Times " + str(size) + " italic", text=self.symbol)

    def move_right(self) -> None:
        self.x += 1

    def move_left(self) -> None:
        self.x -= 1

    def move_up(self) -> None:
        self.y -= 1

    def move_down(self) -> None:
        self.y += 1

    def move(self, way: Ways) -> True:
        """
        Move element in one of the 4 basic ways by updating its coordinates and position
        :param way: Way to move to
        :return: True
        """
        {
            Ways.RIGHT: self.move_right,
            Ways.LEFT: self.move_left,
            Ways.UP: self.move_up,
            Ways.DOWN: self.move_down
        }[way]()
        self.draw()
        return True

    def swap(self, e) -> None:
        """
        Change positions of two elements
        :param e: the other element to change positions with
        :return: None
        """
        self.x, self.y, e.x, e.y = e.x, e.y, self.x, self.y
        self.draw()
        e.draw()

    def draw(self, x: int = -1, y: int = -1) -> None:
        """
        Draw element to its position
        :param x:
        :param x: coordinate
        :param y: coordinate
        :return: None
        """
        if x != -1 and y != -1:
            self.x, self.y = x, y
        self.canvas.coords(self.id,
                           self.x*self.w + self.w/2 + self.w/4*uniform(-1, 1)*self.RAND,
                           self.y*self.h + self.h/2 + self.h/4*uniform(-1, 1)*self.RAND)
