from objects.board import Board
from objects.move import Move
from constants import PIECE_VALUES


class Engine:
    def __init__(self) -> None:
        return

    def search(self, board: Board) -> Move | None:
        _, move = self.minimax(board, 3, -100000, 100000)

        return move

    def minimax(
        self, board: Board, depth: int, alpha: int, beta: int
    ) -> tuple[int, Move | None]:
        if depth == 0:
            return self.evaluate(board), None

        if board.white_to_move:
            max_eval = -100000
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
            min_eval = 100000
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

                # if the piece is white add the value, otherwise subtract the value
                if piece.upper() in PIECE_VALUES:
                    if piece.isupper():
                        score += PIECE_VALUES[piece.upper()]
                    else:
                        score -= PIECE_VALUES[piece.upper()]

        return score
