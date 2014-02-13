#!/usr/bin/env python

"""
Project documentation.
"""

__author__     = "twissell"
__copyright__  = "Copyright 2013, The project-name Project"
__credits__    = ["twissell"]
__license__    = "GPL"
__version__    = "1.0.1"
__maintainer__ = "twissell"
__email__      = "twissel.development@gmail.com"
__status__     = "Prototype"

# import builtins
import sys
import copy
import shelve
import pprint
# import third-party
import pygame
from pygame.locals import QUIT
#from pprint import pprint
# import own


"""
TODO:
    enable 'real' border and padding for tiles
    create more patterns, maybe store them in a external file
    create a pure functional version of pygol
    create a oo version of pygol
    improve the interface with a panel where you can select patterns
    or make your own, enable the posibility to save the game in any
    generation, also let pygol be configurable with things like colors, number of tiles
    per row and columns, size of the tiles, fps and so on...
    add cool music to the game
    let pygol be a screen saver program.
    enable full screen

    implement cell objects as prototypes with a clone method

    read the patterns from a txt file

    intead of square cells let the user choose between square, rounded
    or hexagonal cells.

    let each pattern have his own color in order to see them in a better way

    in order to improve performance of pygol, implement a flyweight design
    pattern.

    do a spaceship video game

    to think of:
        giving a pattern try to find a generator of that pattern ala
        glider gun.

        build a live turing machine

"""

"""
    Concepts:
        a generation is a collection of cells,
        first generation is a special case for generations
        where you can config it with a pattern
"""

# Config


# colors

yellow = (255, 255, 0)
white = (255, 255, 255)
grey = (221, 221, 214)
black = (0, 0, 0)

# screen
SCREEN_WIDTH = 1600
SCREEN_HEIGHT = 1024
SCREEN_COLOR = (grey)

# clock

FPS = 500

# generation

ROWS = 100
COLS = 100

# cells

LIFE_CELL_COLOR = black
DEAD_CELL_COLOR = white

TILE_WIDTH = SCREEN_WIDTH / ROWS
TILE_HEIGHT = SCREEN_HEIGHT / COLS
TILE_MARGIN = 0.5


def save_pattern(pattern, pattern_name):
    patterns = shelve.open('patterns')
    patterns[pattern_name] = pattern


def load_pattern(pattern_name):
    patterns = shelve.open('patterns')
    return patterns[pattern_name]



# empty generation
def empty_generation():
    eg = []
    for i in range(COLS):
        eg.append([])
        for j in range(ROWS):
            eg[i].append('-')
    return eg


def first_generation(pattern=None, start=None):
    # creates an empty generation and populates it
    # with all death cells.
    fg = empty_generation()

    for i in range(len(pattern)):
        fg[start[0] + i][start[1]:(start[1] + len(pattern[i]))] = pattern[i]

    for i in range(len(fg)):
        for j in range(len(fg[i])):
            cell = Cell()
            if fg[i][j] == 'O':
                cell.live = True

            fg[i][j] = cell

    return fg


# each cell has 8 neightbours except those cell
# who are placed in corners. (x, y)

nb = [(1, 0), (-1, 0), (0, 1), (0, -1),
      (-1, -1), (1, -1), (-1, 1), (1, 1)]


def draw_generation(g):

    for i in range(len(g)):
        for j in range(len(g[i])):
            g[i][j].draw(i, j)


def next_generation(prev_generation):

    ng = empty_generation()

    for y in range(len(prev_generation)):
        for x in range(len(prev_generation[y])):

            lc = 0
            # lc -> number of live neightbour cells
            # np -> neightbour position
            # nb -> neightbours positions
            for i in range(len(nb)):
                nx = x + nb[i][0]
                ny = y + nb[i][1]

                try:
                    if prev_generation[ny][nx].live:
                        lc += 1
                except IndexError:
                    pass

            cell = prev_generation[y][x]
            live = judge(cell.live, lc)

            n_cell = copy.copy(cell)

            if live:
                n_cell.live = True
            else:
                n_cell.live = False
            ng[y][x] = n_cell

    return ng


def judge(is_alive, lc):

    live = False

    if is_alive is False:
        if lc == 3:
            live = True
    elif is_alive is True:
        if lc == 3 or lc == 2:
            live = True
        else:
            live = False

    return live


class Cell(object):

    def __init__(self):
        self.live = False

        self.width = TILE_WIDTH
        self.height = TILE_HEIGHT

    def draw(self, y, x):
        if self.live:
            color = LIFE_CELL_COLOR
        else:
            color = DEAD_CELL_COLOR

        y = self.height * y + TILE_MARGIN
        x = self.width * x + TILE_MARGIN
        h = self.height - TILE_MARGIN
        w = self.width - TILE_MARGIN

        pygame.draw.rect(screen, color, (x, y, w, h))

    def __repr__(self):
        return str(self.live)


if __name__ == "__main__":

    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    Clock = pygame.time.Clock()
    g = first_generation(load_pattern('glider_gun'), (50, 50))

    while True:
        screen.fill(SCREEN_COLOR)

        draw_generation(g)
        g = next_generation(g)

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

        pygame.display.update()
        Clock.tick(FPS)
