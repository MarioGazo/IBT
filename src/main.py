"""
This is a main file of my bachelors thesis project.

Subject: Multi-Dimensional Automata and Their Applications in Art
Author: Mário Gažo (xgazom00@vutbr.cz)
Date: Nov 2020 - May 2021

Usage: python main.py [path]
- path: path to the base picture in *.jpg or *.png
"""
from sys import argv
from Base import Base


def main(path) -> None:
    """
    Main function of the project
    """
    Base(path)


if __name__ == "__main__":
    """ START HERE """
    if len(argv) != 2:
        raise Exception('ERR: Wrong argument count')
    main(argv[1])
