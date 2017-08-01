#!/usr/bin/env python3

import collections
import lib

# a coordinate tuple
Coord = collections.namedtuple('Coord', ['x', 'y'])

class Board:
    "Represents the state of the Tetris board."

    def __init__(self, x=10, y=10):
        self.size = Coord(x, y)
        # The board is represented as an array of arrays, with y rows and x columns.
        self.tiles = [[0] * x for _ in range(0, y)]

    def draw(self):
        "Draws the contents of the board with a border around it."
        width, height = self.size

        def tile_char(x, y):
            return "░" if self.tiles[y][x] else " "

        board_border = f'+{"-" * width}+'
        print(board_border)
        for y in range(0, height):
            line = "".join(tile_char(x, y) for x in range(0, width))
            print(f"|{line}|")
        print(board_border)

def main():
    board = Board()

    import atexit
    original_terminal_state = lib.set_terminal_mode()
    atexit.register(lib.restore_terminal, original_terminal_state)

    # This example code draws a horizontal bar 4 squares long.
    row = 2
    board.tiles[row][5] = 1
    board.tiles[row][6] = 1
    board.tiles[row][7] = 1
    board.tiles[row][8] = 1

    board.draw()

    # game loop
    while True:
        deadline = lib.now() + 0.5
        key = lib.get_input(deadline)
        print(key or '.')

if __name__ == '__main__':
    main()
