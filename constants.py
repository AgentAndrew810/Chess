# the default width and height of the window
SCREEN_WIDTH = 840
SCREEN_HEIGHT = 720

# the minimum width and height of the window
MIN_WIDTH = 420
MIN_HEIGHT = 360

# colours
GREEN = (0, 255, 150)
BLUE = (121, 156, 178)
DARK_BLUE = (58, 103, 143)
WHITE = (212, 223, 229)
PINK = (255, 145, 220, 150)
YELLOW = (255, 235, 115)
DARK_YELLOW = (255, 205, 85)
BLACK = (0, 0, 0)

# the offsets for knights, cardinal, and diagonal moves
K_OFFSETS = [(2, 1), (2, -1), (-2, 1), (-2, -1), (1, 2), (1, -2), (-1, 2), (-1, -2)]
C_OFFSETS = [(0, -1), (0, 1), (-1, 0), (1, 0)]
D_OFFSETS = [(-1, -1), (1, 1), (-1, 1), (1, -1)]

# set infinity to one million
INFINITY = 1000000

# the value of pieces
PIECE_VALUES = {"P": 100, "B": 330, "N": 320, "R": 500, "Q": 900, "K": 20000}

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

# the values of the position of each piece, stored as white
PIECE_TABLES = {
    "P": [
        [0, 0, 0, 0, 0, 0, 0, 0],
        [98, 134, 61, 95, 68, 126, 34, -11],
        [-6, 7, 26, 31, 65, 56, 25, -20],
        [-14, 13, 6, 21, 23, 12, 17, -23],
        [-27, -2, -5, 12, 17, 6, 10, -25],
        [-26, -4, -4, -10, 3, 3, 33, -12],
        [-35, -1, -20, -23, -15, 24, 38, -22],
        [0, 0, 0, 0, 0, 0, 0, 0],
    ],
    "N": [
        [-50, -40, -30, -30, -30, -30, -40, -50],
        [-40, -20, 0, 0, 0, 0, -20, -40],
        [-30, 0, 10, 15, 15, 10, 0, -30],
        [-30, 5, 15, 20, 20, 15, 5, -30],
        [-30, 0, 15, 20, 20, 15, 0, -30],
        [-30, 5, 10, 15, 15, 10, 5, -30],
        [-40, -20, 0, 5, 5, 0, -20, -40],
        [-50, -40, -30, -30, -30, -30, -40, -50],
    ],
    "B": [
        [-20, -10, -10, -10, -10, -10, -10, -20],
        [-10, 0, 0, 0, 0, 0, 0, -10],
        [-10, 0, 5, 10, 10, 5, 0, -10],
        [-10, 5, 5, 10, 10, 5, 5, -10],
        [-10, 0, 10, 10, 10, 10, 0, -10],
        [-10, 10, 10, 10, 10, 10, 10, -10],
        [-10, 5, 0, 0, 0, 0, 5, -10],
        [-20, -10, -10, -10, -10, -10, -10, -20],
    ],
    "R": [
        [0, 0, 0, 0, 0, 0, 0, 0],
        [5, 10, 10, 10, 10, 10, 10, 5],
        [-5, 0, 0, 0, 0, 0, 0, -5],
        [-5, 0, 0, 0, 0, 0, 0, -5],
        [-5, 0, 0, 0, 0, 0, 0, -5],
        [-5, 0, 0, 0, 0, 0, 0, -5],
        [-5, 0, 0, 0, 0, 0, 0, -5],
        [0, 0, 0, 5, 5, 0, 0, 0],
    ],
    "Q": [
        [-20, -10, -10, -5, -5, -10, -10, -20],
        [-10, 0, 0, 0, 0, 0, 0, -10],
        [-10, 0, 5, 5, 5, 5, 0, -10],
        [-5, 0, 5, 5, 5, 5, 0, -5],
        [0, 0, 5, 5, 5, 5, 0, -5],
        [-10, 5, 5, 5, 5, 5, 0, -10],
        [-10, 0, 5, 0, 0, 0, 0, -10],
        [-20, -10, -10, -5, -5, -10, -10, -20],
    ],
    "K": [
        [-30, -40, -40, -50, -50, -40, -40, -30],
        [-30, -40, -40, -50, -50, -40, -40, -30],
        [-30, -40, -40, -50, -50, -40, -40, -30],
        [-30, -40, -40, -50, -50, -40, -40, -30],
        [-20, -30, -30, -40, -40, -30, -30, -20],
        [-10, -20, -20, -20, -20, -20, -20, -10],
        [20, 20, 0, 0, 0, 0, 20, 20],
        [20, 30, 10, 0, 0, 10, 30, 20],
    ],
}
