from piece import Piece
from constants import BOARD_SIZE
import copy


class Board:
    def __init__(self):
        self.board = [[0 for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]
        self.initialize_pieces()

    def initialize_pieces(self):
        for row in range(BOARD_SIZE):
            for col in range(BOARD_SIZE):
                if (row + col) % 2 == 1:
                    if row < 3:
                        self.board[row][col] = Piece(1, (row, col))  # Black pieces
                    elif row > 4:
                        self.board[row][col] = Piece(-1, (row, col))  # Red pieces

    def copy(self):
        new_board = Board()
        new_board.board = [[0 for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]
        for row in range(BOARD_SIZE):
            for col in range(BOARD_SIZE):
                piece = self.get_piece(row, col)
                if piece:
                    new_board.board[row][col] = Piece(piece.color, (row, col))
                    new_board.board[row][col].is_king = piece.is_king
        return new_board

    def get_piece(self, row, col):
        if 0 <= row < BOARD_SIZE and 0 <= col < BOARD_SIZE:
            return self.board[row][col]
        return None

    def move_piece(self, start, end):
        start_row, start_col = start
        end_row, end_col = end
        piece = self.board[start_row][start_col]

        # Move the piece
        self.board[end_row][end_col] = piece
        self.board[start_row][start_col] = 0
        piece.move((end_row, end_col))

        # Check if the piece should be kinged
        if (piece.color == 1 and end_row == BOARD_SIZE - 1) or (piece.color == -1 and end_row == 0):
            piece.make_king()

        # Remove captured piece if it's a jump move
        if abs(start_row - end_row) == 2:
            mid_row = (start_row + end_row) // 2
            mid_col = (start_col + end_col) // 2
            self.remove_piece((mid_row, mid_col))

        return self.has_additional_jumps(piece)

    def has_additional_jumps(self, piece):
        valid_jumps = [move for move in self.get_valid_moves(piece) if abs(move[0] - piece.position[0]) == 2]
        return len(valid_jumps) > 0

    def remove_piece(self, position):
        row, col = position
        self.board[row][col] = 0

    def is_valid_move(self, start, end):
        start_row, start_col = start
        end_row, end_col = end
        piece = self.get_piece(start_row, start_col)

        if not piece or self.get_piece(end_row, end_col) != 0:
            return False

        if not (0 <= end_row < BOARD_SIZE and 0 <= end_col < BOARD_SIZE):
            return False

        move_distance = abs(end_row - start_row)
        if move_distance > 2 or abs(end_col - start_col) != move_distance:
            return False

        if piece.color == 1 and not piece.is_king and end_row < start_row:
            return False
        if piece.color == -1 and not piece.is_king and end_row > start_row:
            return False

        if move_distance == 2:
            mid_row, mid_col = (start_row + end_row) // 2, (start_col + end_col) // 2
            captured_piece = self.get_piece(mid_row, mid_col)
            if not captured_piece or captured_piece.color == piece.color:
                return False

        return True

    def get_valid_moves(self, piece):
        valid_moves = []
        row, col = piece.position

        directions = [(-1, -1), (-1, 1), (1, -1), (1, 1)] if piece.is_king else \
            [(-1, -1), (-1, 1)] if piece.color == -1 else [(1, -1), (1, 1)]

        for dir_row, dir_col in directions:
            for distance in [1, 2]:
                end_row, end_col = row + distance * dir_row, col + distance * dir_col
                if self.is_valid_move((row, col), (end_row, end_col)):
                    valid_moves.append((end_row, end_col))

        # If there are jump moves available, only return jump moves
        jump_moves = [move for move in valid_moves if abs(move[0] - row) == 2]
        return jump_moves if jump_moves else valid_moves

    def is_game_over(self):
        black_pieces = red_pieces = 0
        for row in self.board:
            for piece in row:
                if piece:
                    if piece.color == 1:
                        black_pieces += 1
                    else:
                        red_pieces += 1

        return black_pieces == 0 or red_pieces == 0