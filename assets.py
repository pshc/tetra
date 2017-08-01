
tetrominoes = ['O', '-', 'S']

# pixel offsets from the center of rotation
offsets = {
    'O': [(0, 0), (0, 1), (-1, 0), (-1, 1)],

    '-': [(0, 0), (-1, 0), (-2, 0), (1, 0)],
    '|': [(0, 0), (0, 1), (0, 2), (0, -1)],

    'S':  [(0, 0), (1, 0), (0, 1), (-1, 1)],
    'Sv': [(0, 0), (0, -1), (1, 0), (1, 1)],
}

# clockwise rotation mapping
rotations = {
    '-': '|', '|': '-',

    'S': 'Sv', 'Sv': 'S',
}
