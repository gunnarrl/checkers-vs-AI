from board import Board
from player import HumanPlayer, AIPlayer
from utils import get_row_col_from_mouse
from constants import BOARD_SIZE


class GameManager:
    def __init__(self, player1_type, player2_type, ai_difficulty='medium'):
        self.board = Board()
        self.player1 = self._create_player(player1_type, 1, ai_difficulty)
        self.player2 = self._create_player(player2_type, -1, ai_difficulty)
        self.current_player = self.player1
        self.selected_piece = None
        self.multi_jump_in_progress = False


    def _create_player(self, player_type, color, ai_difficulty):
        if player_type == "human":
            return HumanPlayer(color)
        elif player_type == "ai":
            return AIPlayer(color, ai_difficulty)
        else:
            raise ValueError("Invalid player type")

    def switch_turn(self):
        if not self.multi_jump_in_progress:
            self.current_player = self.player2 if self.current_player == self.player1 else self.player1

    def play_turn(self):
        if isinstance(self.current_player, AIPlayer) and not self.multi_jump_in_progress:
            start, end = self.current_player.get_move(self.board)
            self.perform_move(start, end)

    def handle_click(self, pos):
        if isinstance(self.current_player, HumanPlayer):
            row, col = get_row_col_from_mouse(pos)
            piece = self.board.get_piece(row, col)

            if self.selected_piece:
                if (row, col) in self.board.get_valid_moves(self.selected_piece):
                    self.perform_move(self.selected_piece.position, (row, col))
                else:
                    self.selected_piece = None
                    self.multi_jump_in_progress = False
            elif piece and piece.color == self.current_player.color and not self.multi_jump_in_progress:
                self.selected_piece = piece

    def perform_move(self, start, end):
        has_additional_jumps = self.board.move_piece(start, end)
        if has_additional_jumps and abs(start[0] - end[0]) == 2:
            self.multi_jump_in_progress = True
            self.selected_piece = self.board.get_piece(end[0], end[1])
        else:
            self.selected_piece = None
            self.multi_jump_in_progress = False
            self.switch_turn()

    def is_game_over(self):
        black_pieces = 0
        red_pieces = 0
        for row in range(BOARD_SIZE):
            for col in range(BOARD_SIZE):
                piece = self.board.get_piece(row, col)
                if piece:
                    if piece.color == 1:
                        black_pieces += 1
                    else:
                        red_pieces += 1

        return black_pieces == 0 or red_pieces == 0 or not self._player_has_valid_moves(self.current_player.color)

    def _player_has_valid_moves(self, color):
        for row in range(BOARD_SIZE):
            for col in range(BOARD_SIZE):
                piece = self.board.get_piece(row, col)
                if piece and piece.color == color:
                    if self.board.get_valid_moves(piece):
                        return True
        return False

    def get_winner(self):
        if not self.is_game_over():
            return None

        black_pieces = 0
        red_pieces = 0
        for row in range(BOARD_SIZE):
            for col in range(BOARD_SIZE):
                piece = self.board.get_piece(row, col)
                if piece:
                    if piece.color == 1:
                        black_pieces += 1
                    else:
                        red_pieces += 1

        if black_pieces > red_pieces:
            return "Black"
        elif red_pieces > black_pieces:
            return "Red"
        else:
            # In case of a tie (shouldn't happen in standard checkers, but just in case)
            return "Tie"