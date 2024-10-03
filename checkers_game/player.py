import random
from constants import BOARD_SIZE

class HumanPlayer:
    def __init__(self, color):
        self.color = color

    def get_move(self, board):
        # This method will be called by the game manager
        # The actual move selection will be handled in the main game loop
        # through mouse clicks
        pass

class AIPlayer:
    def __init__(self, color, difficulty='medium'):
        self.color = color
        self.difficulty = difficulty
        self.max_depth = self._get_depth_from_difficulty()

    def _get_depth_from_difficulty(self):
        if self.difficulty == 'easy':
            return 2
        elif self.difficulty == 'medium':
            return 4
        else:  # 'very hard'
            return 6

    def get_move(self, board):
        _, best_move = self.minimax(board, self.max_depth, float('-inf'), float('inf'), True)
        return best_move

    def minimax(self, board, depth, alpha, beta, maximizing_player):
        if depth == 0 or board.is_game_over():
            return self.evaluate_board(board), None

        best_move = None
        if maximizing_player:
            max_eval = float('-inf')
            for move in self.get_all_moves(board, self.color):
                board_copy = board.copy()
                board_copy.move_piece(move[0], move[1])
                eval, _ = self.minimax(board_copy, depth - 1, alpha, beta, False)
                if eval > max_eval:
                    max_eval = eval
                    best_move = move
                alpha = max(alpha, eval)
                if beta <= alpha:
                    break
            return max_eval, best_move
        else:
            min_eval = float('inf')
            for move in self.get_all_moves(board, -self.color):
                board_copy = board.copy()
                board_copy.move_piece(move[0], move[1])
                eval, _ = self.minimax(board_copy, depth - 1, alpha, beta, True)
                if eval < min_eval:
                    min_eval = eval
                    best_move = move
                beta = min(beta, eval)
                if beta <= alpha:
                    break
            return min_eval, best_move

    def evaluate_board(self, board):
        score = 0
        for row in range(BOARD_SIZE):
            for col in range(BOARD_SIZE):
                piece = board.get_piece(row, col)
                if piece:
                    if piece.color == self.color:
                        score += 1 + (0.5 if piece.is_king else 0)
                    else:
                        score -= 1 + (0.5 if piece.is_king else 0)
        return score

    def get_all_moves(self, board, color):
        moves = []
        for row in range(BOARD_SIZE):
            for col in range(BOARD_SIZE):
                piece = board.get_piece(row, col)
                if piece and piece.color == color:
                    valid_moves = board.get_valid_moves(piece)
                    moves.extend([((row, col), end) for end in valid_moves])
        return moves