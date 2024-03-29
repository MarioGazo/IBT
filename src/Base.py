from tkinter import Tk, Canvas, NW, Event
from PIL import Image, ImageTk, UnidentifiedImageError
from pathlib import Path
from random import randrange, sample
from Element import Element
from Enums import Effects, Ways, ElementTypes


class Base(Tk):
    """
    Base class represents base picture on which elements are put and moved
    """
    DEBUG = False  # TODO set False
    """ Whether debugging is active """
    SQUARE_SIZE = 30
    """ Approximate cell width and height """
    UPDATES = 3
    """ Number of changes per second """
    elements = []
    """ Elements that are on the base image """

    def __init__(self, path: str) -> None:
        """
        Base picture class constructor
        :param path: Path to base picture (*.png or *.jpg)
        """
        super().__init__()
        self.title('IBT')
        image_path = str(Path(__file__).parent.absolute()) + '/VUT.ico'
        self.iconbitmap(image_path)

        # Base image and canvas to draw onto
        try:
            img_file = Image.open(path)
        except FileNotFoundError:
            raise Exception("Image file not found")
        except UnidentifiedImageError:
            raise Exception("File is not an image")

        # Set the base image and keypress callback
        self.width, self.height = img_file.size
        self.canvas = Canvas(self, width=self.width, height=self.height, background='white', borderwidth=0)
        self.canvas.bind("<KeyPress>", self.keydown)
        self.canvas.pack()
        self.canvas.focus_set()
        bg_image = ImageTk.PhotoImage(img_file)
        self.canvas.create_image(0, 0, anchor=NW, image=bg_image)

        # Calc the amount of cells in horizontal and vertical axis, cell width and height
        self.cells_y = round(self.height / self.SQUARE_SIZE)
        self.cells_x = round(self.cells_y * (self.width / self.height))
        self.cell_h = self.height / self.cells_y
        self.cell_w = self.width / self.cells_x
        if self.DEBUG:  # GRID LINES AND BORDER TO SEE BETTER WHILE DEBUGGING
            self.grid()

        # Generate elements so that they cover 20% of the whole picture
        self.generate_elements(round(self.cells_y * self.cells_x * 0.1))

        # Start movement routine
        self.effect = Effects.FOUR_WAY
        self.movement()
        self.mainloop()

    def keydown(self, event: Event) -> None:
        """
        Callback when key is pressed, map actual effect to pressed button
        :param event: Key press event object
        :return: None
        """
        try:
            # Map the effects to pressed keys
            self.effect = {
                '1': Effects.FOUR_WAY,
                '2': Effects.FOUR_WAY_TYPE,
                '3': Effects.SWAP_TYPE,
                '4': Effects.SCATTER,
                '0': Effects.PAUSE
            }[event.char]
        except KeyError:
            # Didn't press an effect key, ignore
            pass
        finally:
            if self.DEBUG:
                print("Key press: ", event.char)

    def cell_ok(self, x: int, y: int) -> bool:
        """
        Cell is ok to move to if it is not taken or out of border
        :param x: X coord of cell
        :param y: Y coord of cell
        :return: Whether cel is taken, out of automata or not
        """
        # Out of border
        if not (0 < x < self.cells_x - 1 and 0 < y < self.cells_y - 1):
            return False

        # Taken
        for e in self.elements:
            if e.x == x and e.y == y:
                return False

        # Cell is ok
        return True

    def get_free_cell(self) -> tuple:
        """
        Generates tuple of coordinates of random free cell
        :return: tuple of coordinates (x,y)
        """
        # Get random cell
        random_x = randrange(1, self.cells_x - 1)
        random_y = randrange(1, self.cells_y - 1)

        # Find random cell that can be taken over
        while not self.cell_ok(random_x, random_y):
            random_x = randrange(1, self.cells_x - 1)
            random_y = randrange(1, self.cells_y - 1)
        return random_x, random_y

    def generate_set(self, count: int, elem_type: ElementTypes) -> None:
        """
        Generate set of elements of certain type
        :param count: The amount of element to generate
        :param elem_type: Type of elements
        :return: None
        """
        # Generate count amount of elements of elem_type
        for _ in range(count):
            random_x, random_y = self.get_free_cell()
            self.elements.append(Element(self, random_x, random_y, elem_type))

    def generate_elements(self, count: int) -> None:
        """
        Generate random letters and numbers and put them on the base picture
        :param count: The amount of elements of each type
        :return: None
        """
        # Check if element generation is even possible, due to the not fitting the automata
        active_cells = self.cells_x * self.cells_y \
            - 2 * (self.cells_x - 1) \
            - 2 * (self.cells_y - 1)
        coverage = count * 2
        if active_cells < coverage:
            raise ValueError(f"Picture is too small. Active cells = {active_cells}. Cells to cover {coverage}")

        # Generate the same amount of elements of type letter and number
        self.generate_set(count, ElementTypes.LETTER)
        self.generate_set(count, ElementTypes.NUMBER)

    def movement(self) -> None:
        """
        Movement routine, moves them in a certain way and calls itself
        The way the items are used is defined by selected effect
        :return: None
        """
        try:
            # Map the effects to functions, call the appropriate one
            {
                Effects.FOUR_WAY: self.move_4_ways,
                Effects.FOUR_WAY_TYPE: self.move_4_ways,
                Effects.SWAP_TYPE: self.swap,
                Effects.SCATTER: self.scatter,
            }[self.effect]()
        except KeyError:
            # Pause effect is active, ignore
            pass
        finally:
            # Plan the next iteration
            self.after(round(1000/self.UPDATES), self.movement)

    def try_right(self, elem: Element) -> bool or None:
        """
        Try to move the element to the right
        :param elem: element to move
        :return: True if the movement was made, None if not
        """
        if self.cell_ok(elem.x + 1, elem.y):
            return elem.move(Ways.RIGHT)

    def try_left(self, elem: Element) -> bool or None:
        """
        Try to move the element to the left
        :param elem: element to move
        :return: True if the movement was made, None if not
        """
        if self.cell_ok(elem.x - 1, elem.y):
            return elem.move(Ways.LEFT)

    def try_up(self, elem: Element) -> bool or None:
        """
        Try to move the element upwards
        :param elem: element to move
        :return: True if the movement was made, None if not
        """
        if self.cell_ok(elem.x, elem.y - 1):
            return elem.move(Ways.UP)

    def try_down(self, elem: Element) -> bool or None:
        """
        Try to move the element downwards
        :param elem: element to move
        :return: True if the movement was made, None if not
        """
        if self.cell_ok(elem.x, elem.y + 1):
            return elem.move(Ways.DOWN)

    def get_options(self, e: Element) -> list:
        """
        Generates array of ways that the element can move in a random order
        :param e: considered element
        :return: shuffled array of ways
        """
        if self.effect is Effects.FOUR_WAY_TYPE:
            # Arrange effect is active
            if e.elem_type == ElementTypes.LETTER:
                # Letter can't move to the left
                options = range(0, 3)
            else:
                # Number can't move to the right
                options = range(1, 4)
        else:
            # Random effect is active, element can move to any direction
            options = range(0, 4)

        # Shuffle the directions
        return sample(options, len(options))

    def move_4_ways(self) -> None:
        """
        Random/Arrange effect
        Goes through all existing elements and moves them to right, left, up or down,
        either randomly or based on the type of the element
        :return: None
        """
        # Map of the ways to keys from get_options function
        ways = {
            0: lambda x: self.try_right(x),
            1: lambda x: self.try_up(x),
            2: lambda x: self.try_down(x),
            3: lambda x: self.try_left(x)
        }

        # Iterate through all elements, get
        for e in self.elements:
            # Get the movement options, this is where the two effects are distinguished
            options = self.get_options(e)

            # Try to make the moves
            for option in options:

                # Move was made
                if ways[option](e):
                    break

    def swap(self) -> None:
        """
        Effect based on type of the elements, the point is to swap position of two elements of different type
        :return: None
        """
        # Create a copy of the elements array, so elements can be popped
        elements_copy = self.elements.copy()
        while len(elements_copy) > 0:
            # Get two random elements
            random_elements = sample(elements_copy, 2)
            # If their types are different swap them and remove them from elements array copy
            if random_elements[0].elem_type is not random_elements[1].elem_type:
                random_elements[0].swap(random_elements[1])
                elements_copy.remove(random_elements[0])
                elements_copy.remove(random_elements[1])

    def scatter(self) -> None:
        """
        Effect that makes the elements scatter randomly on the base image
        :return: None
        """
        # Make all elements coordinates invalid
        for e in self.elements:
            e.x, e.y = -1, -1

        # Find random free cell for each element
        for e in self.elements:
            x, y = self.get_free_cell()
            e.draw(x, y)

    def grid(self) -> None:
        """
        Creates grid over the base picture and X-es border for debugging purposes
        :return: None
        """
        # Horizontal cells
        for i in range(self.cells_y):
            self.canvas.create_line(0, self.cell_h * i, self.width, self.cell_h * i)
            Element(self, 0, i, ElementTypes.DEBUG)
            Element(self, self.cells_x - 1, i, ElementTypes.DEBUG)

        # Vertical cells
        for i in range(self.cells_x):
            self.canvas.create_line(self.cell_w * i, 0, self.cell_w * i, self.height)
            Element(self, i, 0, ElementTypes.DEBUG)
            Element(self, i, self.cells_y - 1, ElementTypes.DEBUG)
