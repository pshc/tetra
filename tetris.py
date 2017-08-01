#!/usr/bin/env python3

import assets
import collections
import lib
import random

# a coordinate tuple
Coord = collections.namedtuple('Coord', ['x', 'y'])

class Board:
    "Represents the state of the Tetris board."

    def __init__(self, x=10, y=10):
        self.size = Coord(x, y)
        # The board is represented as an array of arrays, with y rows and x columns.
        self.tiles = [[0] * x for _ in range(0, y)]
        # The current falling piece is not stored in the tile array.
        # Instead we store its `center` of rotation and its `kind`.
        self.center = self.kind = None
        self.spawn()

    # TILES

    def draw(self):
        "Draws the contents of the board with a border around it."
        width, height = self.size

        pixels = self.piece_pixels()

        def tile_char(coord):
            if pixels and coord in pixels:
                return "█"
            return "░" if self[coord] else " "

        lib.clear_screen()
        board_border = f'+{"-" * width}+'
        print(board_border)
        for y in range(0, height):
            line = "".join(tile_char(Coord(x, y)) for x in range(0, width))
            print(f"|{line}|")
        print(board_border)

    def __getitem__(self, coord):
        "Returns the (stuck) tile at given (x, y)."
        x, y = coord
        return self.tiles[y][x]

    def __setitem__(self, coord, tile):
        "Writes to the (stuck) tile at given (x, y)."
        x, y = coord
        self.tiles[y][x] = tile

    # FALLING PIECE

    def spawn(self):
        "Spawn a new piece."
        assert self.center is None
        # `self.center` is the center of rotation 
        self.center = Coord(self.size.x//2, 1)
        # pick a random piece out of the seven
        tetromino = random.choice(assets.tetrominoes)
        # and orient it randomly...? todo
        self.kind = tetromino

    def piece_pixels(self):
        "Returns the coords of each pixel of the current falling piece, or None."
        if self.center is None:
            return None
        return [add_coords(self.center, off) for off in assets.offsets[self.kind]]

    def shift(self, offset):
        "Move the piece horizontally."
        # detect sideways collision
        for x, y in self.piece_pixels():
            if x + offset < 0 or x + offset >= self.size.x: # hit a board edge?
                return
            elif self[x + offset, y]: # hit a stuck tile?
                return
        # otherwise, we're good!
        self.center = Coord(self.center.x + offset, self.center.y)
        self.draw()

    def descend(self):
        "Move the piece down one space."
        stuck = False
        pixels = self.piece_pixels()
        for x, y in pixels:
            if y >= self.size.y - 1: # hit bottom of board?
                stuck = True
                break
            elif self[x, y+1]: # hit a stuck tile?
                stuck = True
                break

        if stuck:
            for coord in pixels:
                self[coord] = 1
            self.center = self.kind = None
        else:
            self.center = Coord(self.center.x, self.center.y + 1)


def add_coords(a, b):
    "Add the components of two coords together."
    xa, ya = a
    xb, yb = b
    return xa + xb, ya + yb

def main():
    board = Board()

    import atexit
    original_terminal_state = lib.set_terminal_mode()
    atexit.register(lib.restore_terminal, original_terminal_state)

    # game loop
    delay = 2
    while True:
        board.draw()

        # if nothing's falling, wait a bit then spawn a piece
        if board.kind is None:
            lib.get_input(lib.now() + delay)
            board.spawn()
            continue

        # let the player shift and rotate freely before the next down-step
        deadline = lib.now() + delay
        key = None
        while key != 'down':
            key = lib.get_input(deadline)
            if key == 'left':
                board.shift(-1)
            elif key == 'right':
                board.shift(1)
            else:
                break

        # down-step
        board.descend()


if __name__ == '__main__':
    main()
