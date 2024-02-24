from objects.board import Board
from objects.move import Move
from constants import (
    PIECE_VALUES,
    KNIGHTS_TABLE,
    BISHOPS_TABLE,
    ROOKS_TABLE,
    QUEEN_TABLE,
    KING_TABLE_WHITE,
    KING_TABLE_BLACK,
)


class Engine:
    def __init__(self) -> None:
        return

    def search(self, board: Board) -> Move | None:
        _, move = self.minimax(board, 3, -1000000, 1000000)
        print(_)

        return move

    def minimax(
        self, board: Board, depth: int, alpha: int, beta: int
    ) -> tuple[int, Move | None]:
        if depth == 0:
            return self.evaluate(board), None

        if board.white_to_move:
            max_eval = -1000000
            best_move = None

            for move in board.get_legal_moves():
                child = board.make_move(move)
                eval = self.minimax(child, depth - 1, alpha, beta)[0]

                if eval > max_eval:
                    max_eval = eval
                    best_move = move

                alpha = max(alpha, eval)
                if alpha >= beta:
                    break

            return max_eval, best_move

        else:
            min_eval = 1000000
            best_move = None

            for move in board.get_legal_moves():
                child = board.make_move(move)
                eval = self.minimax(child, depth - 1, alpha, beta)[0]

                if eval < min_eval:
                    min_eval = eval
                    best_move = move

                beta = min(beta, eval)
                if beta <= alpha:
                    break

            return min_eval, best_move

    def evaluate(self, board: Board) -> int:
        score = 0

        for rank in range(8):
            for file in range(8):
                piece = board.board[rank][file]

                # skip blank squares
                if not piece:
                    continue

                # get 1 if white, else -1
                plus_minus = 1 if piece.isupper() else -1
                piece = piece.upper()

                # add or subtract the value of the piece
                score += plus_minus * PIECE_VALUES[piece]

                # add points based on position on board
                if piece == "N":
                    score += plus_minus * KNIGHTS_TABLE[rank][file]

                elif piece == "B":
                    score += plus_minus * BISHOPS_TABLE[rank][file]

                elif piece == "R":
                    score += plus_minus * ROOKS_TABLE[rank][file]

                elif piece == "Q":
                    score += plus_minus * QUEEN_TABLE[rank][file]

                elif piece == "K":
                    if plus_minus == 1:
                        score += KING_TABLE_WHITE[rank][file]
                    else:
                        score -= KING_TABLE_BLACK[rank][file]

        return score
