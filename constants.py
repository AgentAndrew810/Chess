# the default width and height of the window
SCREEN_WIDTH = 840
SCREEN_HEIGHT = 720

# the minimum width and height of the window
MIN_WIDTH = 420
MIN_HEIGHT = 360

# colours
BLUE = (121, 156, 178)
WHITE = (212, 223, 229)
PINK = (255, 145, 220, 150)
YELLOW = (255, 235, 115)
DARK_YELLOW = (255, 205, 85)
BLACK = (0, 0, 0)

# the offsets for knights, cardinal, and diagonal moves
K_OFFSETS = [(2, 1), (2, -1), (-2, 1), (-2, -1), (1, 2), (1, -2), (-1, 2), (-1, -2)]
C_OFFSETS = [(0, -1), (0, 1), (-1, 0), (1, 0)]
D_OFFSETS = [(-1, -1), (1, 1), (-1, 1), (1, -1)]

# the value of pieces
PIECE_VALUES = {"P": 1, "B": 3, "N": 3, "R": 5, "Q": 9, "K": 1000}

# starting chess position
CHESS_POSITION = [
    ["r", "n", "b", "q", "k", "b", "n", "r"],
    ["p", "p", "p", "p", "p", "p", "p", "p"],
    ["", "", "", "", "", "", "", ""],
    ["", "", "", "", "", "", "", ""],
    ["", "", "", "", "", "", "", ""],
    ["", "", "", "", "", "", "", ""],
    ["P", "P", "P", "P", "P", "P", "P", "P"],
    ["R", "N", "B", "Q", "K", "B", "N", "R"],
]
