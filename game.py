import pygame
import time
from objects.engine import Engine
from objects.board import Board
from objects.drawnobject import DrawnObject
from constants import BLUE, WHITE, PINK, FEN


class Game(DrawnObject):
    def __init__(self) -> None:
        super().__init__()
        self.load_images()

        self.active = True
        self.player_is_white = True
        self.held_piece = None

        self.engine = Engine()
        self.board = Board.from_fen(FEN)
        self.next_moves = self.board.get_moves()

    def update(self) -> None:
        self.load_images()

    @property
    def player_to_move(self) -> bool:
        return self.board.white_to_move == self.player_is_white

    def get_x(self, file: int) -> int:
        _, file = self.flip_coordinates(0, file)
        return self.x_padd + self.square_size * file

    def get_y(self, rank: int) -> int:
        rank, _ = self.flip_coordinates(rank, 0)
        return self.y_padd + self.square_size * rank

    def flip_coordinates(self, rank: int, file: int) -> tuple[int, int]:
        # if the player is white return the normal rank and file
        # otherwise return inverted rank and file
        if self.player_is_white:
            return (rank, file)
        else:
            return (7 - rank, 7 - file)

    def grab_piece(self, x: int, y: int) -> None:
        # check if the mouse is outside the board
        if not (self.x_padd < x < self.x_padd + self.board_size):
            if not (self.y_padd < y < self.y_padd + self.board_size):
                return

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

    def drop_piece(self, x: int, y: int) -> None:
        # get the rank and file
        rank = (y - self.y_padd) // self.square_size
        file = (x - self.x_padd) // self.square_size

        # flip rank and file if playing as black
        rank, file = self.flip_coordinates(rank, file)

        # if the move is a valid move
        for move in self.next_moves:
            if move.old_pos == self.held_piece:
                if (rank, file) == move.new_pos:
                    self.board = self.board.make_move(move)

        self.held_piece = None

    def make_computer_move(self) -> None:
        t = time.time()
        move = self.engine.search(self.board)
        self.board = self.board.make_move(move)
        self.next_moves = self.board.get_moves()
        print(f"Time to make Move: {round(time.time()-t, 2)}s")

    def draw(self, screen: pygame.surface.Surface) -> None:
        screen.fill((75, 100, 145))

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

        # get all the attacked positions
        attack_moves = [
            move.new_pos for move in self.next_moves if move.old_pos == self.held_piece
        ]

        for rank in range(8):
            for file in range(8):
                piece = self.board.board[rank][file]

                # draw the piece
                if piece and (rank, file) != self.held_piece:
                    screen.blit(
                        self.images[piece], (self.get_x(file), self.get_y(rank))
                    )

                # draw a circle if the held piece can move to that square
                if (rank, file) in attack_moves:
                    # determine the radius and width based on if its attacking a piece
                    if piece:
                        # circle outline on piece
                        radius = round(self.square_size / 2.5)
                        width = self.square_size // 14
                    else:
                        # dot on square
                        radius = self.square_size // 6
                        width = 0

                    # create a surface and draw the circle on it
                    surface = pygame.Surface((radius * 2, radius * 2), pygame.SRCALPHA)
                    pygame.draw.circle(surface, PINK, (radius, radius), radius, width)

                    # draw the surface onto the screen
                    x = self.get_x(file) + 0.5 * self.square_size - radius
                    y = self.get_y(rank) + 0.5 * self.square_size - radius
                    screen.blit(surface, (x, y))

        # if holding a piece
        if self.held_piece is not None:
            rank, file = self.held_piece
            piece = self.board.board[rank][file]
            mouse_x, mouse_y = pygame.mouse.get_pos()

            # draw the held piece adjusted for mouse offset
            screen.blit(
                self.images[piece], (mouse_x - self.x_offset, mouse_y - self.y_offset)
            )

        # draw board outline
        pygame.draw.rect(
            screen,
            (0, 0, 0),
            (self.x_padd, self.y_padd, self.board_size, self.board_size),
            3,
        )

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
