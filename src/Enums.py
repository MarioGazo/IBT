from enum import Enum


class Effects(Enum):
    """
    Effects of two-dimensional automata effects (the way the elements are moved)
    """
    PAUSE = 0
    """ Elements are not moving """
    FOUR_WAY = 1
    """ Elements are moving in random directions """
    FOUR_WAY_TYPE = 2
    """ Elements are sliding to the left or right, based on their type """
    SWAP_TYPE = 3
    """ Elements of different types are swapping places """
    SCATTER = 4
    """ Elements are dispersed randomly """


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
