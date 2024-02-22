import pygame
from objects.board import Board
from objects.drawnobject import DrawnObject
from constants import BLUE, WHITE, FEN


class Game(DrawnObject):
    def __init__(self) -> None:
        super().__init__()

        print(self.__dict__)

        self.load_images()

        self.board = Board.from_fen(FEN)
        self.active = True
        self.player_is_white = False

    def update(self) -> None:
        self.load_images()

    @property
    def player_to_move(self) -> bool:
        return self.board.white_to_move == self.player_is_white

    def get_x(self, file: int) -> int:
        return self.x_padd + self.square_size * file

    def get_y(self, rank: int) -> int:
        return self.y_padd + self.square_size * rank

    def flip_coordinates(self, rank: int, file: int) -> tuple[int, int]:
        # if the player is white return the normal rank and file
        # otherwise return inverted rank and file
        if self.player_is_white:
            return (rank, file)
        else:
            return (7 - rank, 7 - file)

    def grab_piece(self, x: int, y: int) -> None:
        # get the rank and file grabbed and their offsets
        rank, self.y_offset = divmod(y - self.y_padd, self.square_size)
        file, self.x_offset = divmod(x - self.x_padd, self.square_size)

        # flip rank and file if playing as black
        rank, file = self.flip_coordinates(rank, file)
        piece = self.board.board[rank][file]

        # check if grabbing the correct colour
        if (piece.isupper() and self.board.white_to_move) or (
            piece.islower() and not self.board.white_to_move
        ):
            self.held_piece = (rank, file)

    def draw(self, screen: pygame.surface.Surface) -> None:
        # draw the checkerboard
        for rank in range(8):
            for file in range(8):
                # determine colour of square based on if the sum of the rank and file is even or odd
                colour = WHITE if (rank + file) % 2 == 0 else BLUE

                # draw the square
                pygame.draw.rect(
                    screen,
                    colour,
                    (
                        self.get_x(file),
                        self.get_y(rank),
                        self.square_size,
                        self.square_size,
                    ),
                )

        for pos in range(64):
            # flip rank and file if playing as black
            rank, file = self.flip_coordinates(pos // 8, pos % 8)
            piece = self.board.board[pos]

            # draw the piece
            if piece is not None:
                screen.blit(self.images[piece], (self.get_x(file), self.get_y(rank)))

    def load_images(self) -> None:
        # load each piece where the key is the char stored in the board
        self.images = {
            "P": pygame.image.load("assets/white-pawn.png"),
            "N": pygame.image.load("assets/white-knight.png"),
            "B": pygame.image.load("assets/white-bishop.png"),
            "R": pygame.image.load("assets/white-rook.png"),
            "Q": pygame.image.load("assets/white-queen.png"),
            "K": pygame.image.load("assets/white-king.png"),
            "p": pygame.image.load("assets/black-pawn.png"),
            "n": pygame.image.load("assets/black-knight.png"),
            "b": pygame.image.load("assets/black-bishop.png"),
            "r": pygame.image.load("assets/black-rook.png"),
            "q": pygame.image.load("assets/black-queen.png"),
            "k": pygame.image.load("assets/black-king.png"),
        }

        # resize the image to square_size
        for image in self.images:
            self.images[image] = pygame.transform.scale(
                self.images[image], (self.square_size, self.square_size)
            )
