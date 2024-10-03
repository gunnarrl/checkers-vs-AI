import pygame
from constants import WINDOW_SIZE, BOARD_SIZE, SQUARE_SIZE, BLACK, WHITE, RED, CROWN, GREY


class GameRenderer:
    def __init__(self, window):
        self.window = window

    def draw_board(self, board):
        self.window.fill(WHITE)
        for row in range(BOARD_SIZE):
            for col in range(BOARD_SIZE):
                if (row + col) % 2 == 0:
                    pygame.draw.rect(self.window, WHITE, (col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))
                else:
                    pygame.draw.rect(self.window, GREY, (col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))

    def draw_pieces(self, board):
        for row in range(BOARD_SIZE):
            for col in range(BOARD_SIZE):
                piece = board.get_piece(row, col)
                if piece:
                    color = BLACK if piece.color == 1 else RED
                    pygame.draw.circle(self.window, color, 
                                       (col * SQUARE_SIZE + SQUARE_SIZE // 2, 
                                        row * SQUARE_SIZE + SQUARE_SIZE // 2), 
                                       SQUARE_SIZE // 2 - 10)
                    if piece.is_king:
                        self.window.blit(CROWN, 
                                         (col * SQUARE_SIZE + SQUARE_SIZE // 2 - CROWN.get_width() // 2, 
                                          row * SQUARE_SIZE + SQUARE_SIZE // 2 - CROWN.get_height() // 2))

    def draw_valid_moves(self, valid_moves):
        for move in valid_moves:
            row, col = move
            pygame.draw.circle(self.window, (0, 255, 0), 
                               (col * SQUARE_SIZE + SQUARE_SIZE // 2, 
                                row * SQUARE_SIZE + SQUARE_SIZE // 2), 
                               15)

    def draw_selected_piece(self, piece):
        row, col = piece.position
        pygame.draw.circle(self.window, (0, 0, 255), 
                           (col * SQUARE_SIZE + SQUARE_SIZE // 2, 
                            row * SQUARE_SIZE + SQUARE_SIZE // 2), 
                           SQUARE_SIZE // 2)

    def update_display(self):
        pygame.display.update()