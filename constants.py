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
YELLOW = (255, 255, 175)
BLACK = (0, 0, 0)

# the offsets for knights, cardinal, and diagonal moves
K_OFFSETS = [(2, 1), (2, -1), (-2, 1), (-2, -1), (1, 2), (1, -2), (-1, 2), (-1, -2)]
C_OFFSETS = [(0, -1), (0, 1), (-1, 0), (1, 0)]
D_OFFSETS = [(-1, -1), (1, 1), (-1, 1), (1, -1)]

# the value of pieces
PIECE_VALUES = {"P": 1, "B": 3, "N": 3, "R": 5, "Q": 9, "K": 1000}

# starting position fen
FEN = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR"
# FEN = "r1bk3r/p2pBpNp/n4n2/1p1NP2P/6P1/3P4/P1P1K3/q5b1"
