# all of the different kinds of tetronimoes and their orientations
tetrominoes = [
    'O',
    ('-', '|'),
    # `v`ertical
    ('S', 'Sv'),
    ('Z', 'Zv'),
    # four-way rotations use NWES notation
    ('Le', 'Ln', 'Lw', 'Ls'),
    ('Jw', 'Js', 'Je', 'Jn'),
    ('Ts', 'Te', 'Tn', 'Tw'),
]

# pixel offsets from the center of rotation
# note: every configuration includes (0, 0) so we omit it
offsets = {
    'O': [(0, 1), (-1, 0), (-1, 1)],

    '-': [(-1, 0), (-2, 0), (1, 0)],
    '|': [(0, 1), (0, 2), (0, -1)],

    #  xx
    # xx
    'S':  [(1, 0), (0, 1), (-1, 1)],
    'Sv': [(0, -1), (1, 0), (1, 1)],

    # xx
    #  xx
    'Z':  [(-1, 0), (0, 1), (1, 1)],
    'Zv': [(0, 1), (1, 0), (1, -1)],

    # xxx
    # x
    'Le': [(1, 0), (-1, 0), (-1, 1)],
    'Ln': [(0, -1), (0, 1), (1, 1)],
    'Lw': [(-1, 0), (1, 0), (1, -1)],
    'Ls': [(0, 1), (0, -1), (-1, -1)],

    # xxx
    #   x
    'Jw': [(-1, 0), (1, 0), (1, 1)],
    'Js': [(0, 1), (0, -1), (1, -1)],
    'Je': [(1, 0), (-1, 0), (-1, -1)],
    'Jn': [(0, -1), (0, 1), (-1, 1)],

    # xxx
    #  x
    'Ts': [(0, 1), (-1, 0), (1, 0)],
    'Te': [(1, 0), (0, 1), (0, -1)],
    'Tn': [(0, -1), (1, 0), (-1, 0)],
    'Tw': [(-1, 0), (0, -1), (0, 1)],
}

# maps each kind to the next (ccw) rotation
rotations = {
    '-': '|', '|': '-',
    'S': 'Sv', 'Sv': 'S',
    'Z': 'Zv', 'Zv': 'Z',
    'Le': 'Ln', 'Ln': 'Lw', 'Lw': 'Ls', 'Ls': 'Le',
    'Jw': 'Js', 'Js': 'Je', 'Je': 'Jn', 'Jn': 'Jw',
    'Ts': 'Te', 'Te': 'Tn', 'Tn': 'Tw', 'Tw': 'Ts',
}
