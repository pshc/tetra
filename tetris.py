#!/usr/bin/env python3

import assets
import collections
import lib
import random

# a coordinate tuple
Coord = collections.namedtuple('Coord', ['x', 'y'])

class Board:
    "Represents the state of the Tetris board."

    size = Coord(10, 16)
    # hide two lines at the top for some extra wiggle room
    vanish_zone = 2

    def __init__(self):
        self.alive = True
        self.stats = Stats()
        # The board is represented as an array of arrays, with y rows and x columns.
        x, y = self.size
        self.tiles = [[0] * x for _ in range(0, y)]
        # The current falling piece is not stored in the tile array.
        # Instead we store its `center` of rotation and its `kind`.
        self.center = self.kind = None
        self.spawn()

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
        for y in range(self.vanish_zone, height):
            line = "".join(tile_char(Coord(x, y)) for x in range(0, width))
            print(f"|{line}|", end='')
            self.stats.draw(y - self.vanish_zone)
        print(board_border)

    # TILES

    def clear_lines(self):
        "Find and remove any fully occupied rows."
        for y in range(0, self.size.y):
            if all(self.tiles[y]):
                # move all the rows above this down
                self.tiles.pop(y)
                self.tiles.insert(0, [0] * self.size.x)
                self.stats.lines += 1

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

        # pick a random piece out of the seven
        tetromino = random.choice(assets.tetrominoes)
        self.kind = tetromino

        # try to find a free space to spawn this piece
        # first, find the top edge
        top = self.vanish_zone + max(-y for x, y in assets.offsets[tetromino])
        mid = self.size.x//2
        # give a little wiggle room when the board is full
        for y in (top, top - 1):
            for x in (mid, mid + 1, mid - 1):
                if self.pixels_free(pixels(tetromino, (x, y))):
                    self.center = Coord(x, y)
                    return
        # oh no
        self.alive = False
        self.center = (mid, top)

    def piece_pixels(self):
        "Returns the coords of each pixel of the current falling piece, or None."
        if self.center is None:
            return None
        return pixels(self.kind, self.center)

    def pixels_free(self, pixels):
        "Returns True if all the given pixels are valid open positions in the board."
        for pixel in pixels:
            x, y = pixel
            if x < 0 or x >= self.size.x:
                return False
            if y < 0 or y >= self.size.y:
                return False
            if self[pixel]:
                return False
        return True

    def rotate(self):
        "Rotate the piece (counter-clockwise)."
        rotated = assets.rotations.get(self.kind)
        if rotated is None:
            return
        # `dest` will be set to a position where this piece fits
        dest = None
        if self.pixels_free(pixels(rotated, self.center)):
            dest = self.center
        else:
            # attempt to wall kick by checking left and right
            left = add_coords(self.center, (1, 0))
            right = add_coords(self.center, (-1, 0))
            if self.pixels_free(pixels(rotated, left)):
                dest = left
            elif self.pixels_free(pixels(rotated, right)):
                dest = right

        # extra wide wall kick for the oooo piece
        if rotated == '-' and dest is None:
            left = add_coords(self.center, (2, 0))
            right = add_coords(self.center, (-2, 0))
            if self.pixels_free(pixels(rotated, left)):
                dest = left
            elif self.pixels_free(pixels(rotated, right)):
                dest = right

        if dest is not None:
            self.kind = rotated
            self.center = dest
            self.draw()

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

    def hard_drop(self):
        "Moves the piece all the way down."
        while self.kind is not None:
            self.descend()
        self.draw()

class Stats:
    "Statistics for a single game."
    lines = 0

    def draw(self, y):
        "Draw the stats display to the right of the board, at line `y`."
        if y == 0:
            print(f"  Lines: {self.lines}")
        else:
            print()

def pixels(kind, center):
    "Return all the individual pixel positions for the given piece."
    # note: the center is always filled. the rest of the pixels come from our lookup table
    return [center] + [add_coords(center, xy) for xy in assets.offsets[kind]]

def add_coords(a, b):
    "Add the components of two coords together."
    xa, ya = a
    xb, yb = b
    return Coord(xa + xb, ya + yb)

def main():
    board = Board()

    import atexit
    original_terminal_state = lib.set_terminal_mode()
    atexit.register(lib.restore_terminal, original_terminal_state)

    # game loop
    delay = 2
    while board.alive:
        board.draw()

        # if nothing's falling, wait a bit then spawn a piece
        if board.kind is None:
            lib.get_input(lib.now() + delay)
            if board.clear_lines():
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
            elif key == 'up':
                board.rotate()
            elif key == 'space':
                board.hard_drop()
                break
            else:
                break

        # down-step
        if board.kind is not None:
            board.descend()

    board.draw()
    print()
    print('GAME OVER!')

if __name__ == '__main__':
    main()
