import time
from objects.board import Board
from objects.move import Move
from constants import PIECE_VALUES, PIECE_TABLES, INFINITY


class Engine:
    def __init__(self) -> None:
        self.WHITE_PIECE_TABLES = PIECE_TABLES
        self.BLACK_PIECE_TABLES = {}

        # reverse the order of the outer list in each table for black
        for piece, table in PIECE_TABLES.items():
            reversed_table = table[::-1]
            self.BLACK_PIECE_TABLES[piece.lower()] = reversed_table

    def search(self, board: Board) -> Move | None:
        current_time = time.time()

        eval, move = self.minimax(board, 3, -INFINITY, INFINITY)

        if eval > 0:
            print(f"White is up {round(eval/100, 2)} pieces!")
        else:
            print(f"Black is up {round(-eval/100, 2)} pieces!")

        print(f"Computer Move Time: {round(time.time()-current_time, 3)}\n")

        return move

    def minimax(
        self, board: Board, depth: int, alpha: int, beta: int
    ) -> tuple[int, Move | None]:
        if depth == 0:
            return self.evaluate(board), None

        if board.white_to_move:
            best_eval = -INFINITY
            best_move = None

            for move in board.get_legal_moves():
                child = board.make_move(move)

                eval = self.minimax(child, depth - 1, alpha, beta)[0]

                if eval >= best_eval:
                    best_eval = eval
                    best_move = move

                alpha = max(alpha, eval)
                if beta <= alpha:
                    break

        else:
            best_eval = INFINITY
            best_move = None

            for move in board.get_legal_moves():
                child = board.make_move(move)
                eval = self.minimax(child, depth - 1, alpha, beta)[0]

                if eval <= best_eval:
                    best_eval = eval
                    best_move = Move(
                        move.old_rank, move.old_file, move.new_rank, move.new_file
                    )

                beta = min(beta, eval)
                if beta <= alpha:
                    break

        return best_eval, best_move

    def evaluate(self, board: Board) -> int:
        score = 0

        for rank in range(8):
            for file in range(8):
                piece = board.board[rank][file]

                # skip blank squares
                if not piece:
                    continue

                if piece.isupper():
                    score += PIECE_VALUES[piece]
                    score += self.WHITE_PIECE_TABLES[piece][rank][file]
                else:
                    score -= PIECE_VALUES[piece.upper()]
                    score -= self.BLACK_PIECE_TABLES[piece][rank][file]

        return score
