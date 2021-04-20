from enum import Enum


class Effects(Enum):
    """
    Effects of two-dimensional automata effects (the way the elements are moved)
    """
    """ Elements are not moving """
    PAUSE = 0
    """ Elements are moving in random directions """
    RANDOM = 1
    """ Elements are sliding to the left or right, based on their type """
    ARRANGE = 2
    """ Elements of different types are swapping places """
    ALTERNATE = 3
    """ Elements are dispersed randomly """
    SCATTER = 4


class Ways(Enum):
    """
    Basic ways
    """
    RIGHT = 0
    LEFT = 1
    UP = 2
    DOWN = 3


class ElementTypes(Enum):
    """
    Types of elements that are moved
    """
    LETTER = 0
    NUMBER = 1
    DEBUG = 99
