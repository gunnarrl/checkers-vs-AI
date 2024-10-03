import pygame
import sys
from game_manager import GameManager
from graphics import GameRenderer
from constants import WINDOW_SIZE, WHITE, BLACK, RED, GREY, GREEN


def draw_text(surface, text, size, x, y, color=BLACK):
    font = pygame.font.Font(None, size)
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect()
    text_rect.center = (x, y)
    surface.blit(text_surface, text_rect)


def draw_button(surface, text, x, y, width, height, color, text_color=BLACK):
    pygame.draw.rect(surface, color, (x, y, width, height))
    draw_text(surface, text, 30, x + width // 2, y + height // 2, text_color)
    return pygame.Rect(x, y, width, height)


def entry_screen(window):
    player_count = 1
    human_color = 1  # 1 for black, -1 for red
    ai_difficulty = 'medium'

    while True:
        window.fill(WHITE)
        draw_text(window, "Checkers", 60, WINDOW_SIZE // 2, 100)

        player_button = draw_button(window, f"Players: {player_count}", WINDOW_SIZE // 2 - 100, 200, 200, 50, GREY)
        color_button = draw_button(window, f"Human Color: {'Black' if human_color == 1 else 'Red'}",
                                   WINDOW_SIZE // 2 - 100, 270, 200, 50, GREY)
        difficulty_button = draw_button(window, f"AI Difficulty: {ai_difficulty.capitalize()}", WINDOW_SIZE // 2 - 100,
                                        340, 200, 50, GREY)
        start_button = draw_button(window, "Start Game", WINDOW_SIZE // 2 - 100, 410, 200, 50, RED, WHITE)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if player_button.collidepoint(mouse_pos):
                    player_count = 3 - player_count  # Toggle between 1 and 2
                elif color_button.collidepoint(mouse_pos):
                    human_color *= -1  # Toggle between 1 and -1
                elif difficulty_button.collidepoint(mouse_pos):
                    if ai_difficulty == 'easy':
                        ai_difficulty = 'medium'
                    elif ai_difficulty == 'medium':
                        ai_difficulty = 'very hard'
                    else:
                        ai_difficulty = 'easy'
                elif start_button.collidepoint(mouse_pos):
                    return player_count, human_color, ai_difficulty

        pygame.display.update()


def win_screen(window, winner):
    while True:
        window.fill(WHITE)
        draw_text(window, f"{winner} Wins!", 60, WINDOW_SIZE // 2, WINDOW_SIZE // 2 - 50)
        play_again_button = draw_button(window, "Play Again", WINDOW_SIZE // 2 - 100, WINDOW_SIZE // 2 + 50, 200, 50,
                                        GREEN)
        quit_button = draw_button(window, "Quit", WINDOW_SIZE // 2 - 100, WINDOW_SIZE // 2 + 120, 200, 50, RED)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if play_again_button.collidepoint(mouse_pos):
                    return True
                elif quit_button.collidepoint(mouse_pos):
                    return False

        pygame.display.update()


def main():

    pygame.init()
    window = pygame.display.set_mode((WINDOW_SIZE, WINDOW_SIZE))
    pygame.display.set_caption("Checkers")

    while True:
        player_count, human_color, ai_difficulty = entry_screen(window)

        player1_type = "human"
        player2_type = "human" if player_count == 2 else "ai"

        if player_count == 1 and human_color == -1:
            player1_type, player2_type = player2_type, player1_type

        game_manager = GameManager(player1_type, player2_type, ai_difficulty)
        renderer = GameRenderer(window)

        clock = pygame.time.Clock()

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    pos = pygame.mouse.get_pos()
                    game_manager.handle_click(pos)

            game_manager.play_turn()

            renderer.draw_board(game_manager.board)
            renderer.draw_pieces(game_manager.board)

            if game_manager.selected_piece:
                renderer.draw_selected_piece(game_manager.selected_piece)
                valid_moves = game_manager.board.get_valid_moves(game_manager.selected_piece)
                renderer.draw_valid_moves(valid_moves)

            renderer.update_display()

            if game_manager.is_game_over():
                winner = game_manager.get_winner()
                if win_screen(window, winner):
                    break  # Start a new game
                else:
                    pygame.quit()
                    sys.exit()

            clock.tick(60)


if __name__ == "__main__":
    main()