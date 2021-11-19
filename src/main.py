import pygame
from time import sleep
from tkinter import *
from tkinter import messagebox
from Amazons import Amazons
from Board import Board
from AI import AI

board = Board()
amazons = Amazons()
ai = AI()

game_board = board.get_board()

WIDTH = 50
HEIGHT = 50
MARGIN = 1

BLACK = (60, 60, 60)
BROWN = (204, 102, 0)
LIGHT_BROWN = (205, 184, 133)
RED = (255, 60, 90)
LIGHT_RED = (245, 120, 120)

pygame.init()
WINDOW_SIZE = [10 * WIDTH + 11 * MARGIN, 10 * HEIGHT + 11 * MARGIN]
screen = pygame.display.set_mode(WINDOW_SIZE)
pygame.display.set_caption("Game of Amazons")
intro_screen = pygame.image.load(r'pieces/intro_screen.png')
clock = pygame.time.Clock()


def text_objects(text, font):
    text_surface = font.render(text, True, (0, 0, 0))
    return text_surface, text_surface.get_rect()


def button(x, y, width, height, color1, color2, text_msg, param, function=None):
    pos = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()

    if x + width > pos[0] > x and y + height > pos[1] > y:
        pygame.draw.rect(screen, color2, (x, y, width, height))
        if click[0] == 1 and function is not None:
            if param is not None:
                return function(param)
            else:
                return function()

    else:
        pygame.draw.rect(screen, color1, (x, y, width, height))

    small_text = pygame.font.Font("freesansbold.ttf", 20)
    text_surf, text_rect = text_objects(text_msg, small_text)
    text_rect.center = ((x + (width / 2)), (y + (height / 2)))
    screen.blit(text_surf, text_rect)


def quit_game():
    pygame.quit()
    quit()


def is_finished(current_board, player_vs_player):
    if amazons.finished(current_board):
        player = amazons.get_winner()

        # The player who loses will start the next game
        if player == "Black":
            amazons.black_won()
            amazons.set_params(0, 0, 0)
        else:
            amazons.white_won()
            amazons.set_params(3, 0, 0)

        Tk().wm_withdraw()
        messagebox.showinfo('The game has ended', f'{player} player won!\n\nWhite: {amazons.get_white_wins()}'
                            f'\nBlack: {amazons.get_black_wins()}')
        sleep(0.75)
        board.initialize_board(current_board)
        board.draw_board(current_board, WIDTH, HEIGHT, MARGIN,
                         screen, amazons.get_turn(), player_vs_player)


def game_intro():
    intro = True

    while intro:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                intro = not intro
                pygame.quit()
                quit()

        screen.fill((0, 0, 0))
        screen.blit(intro_screen, (0, 0))

        button((WIDTH * 10 + 11) / 2 - 85, 250, 170, 50, BROWN,
               LIGHT_BROWN, "Player vs. Player", True, game_loop)
        button((WIDTH * 10 + 11)/2 - 75, 350, 150, 50, BROWN,
               LIGHT_BROWN, "Player vs. CPU", False, game_loop)
        button((WIDTH * 10 + 11)/2 - 50, 450, 100, 50,
               RED, LIGHT_RED, "Quit", None, quit_game)

        pygame.display.update()
        clock.tick(60)


def game_loop(player_vs_player):
    screen.fill(BLACK)
    amazons.set_params(0, 0, 0)
    board.initialize_board(game_board)

    done = False
    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit_game()

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    amazons.zero_wins()
                    done = True

            elif not player_vs_player and amazons.get_turn() == 3:
                amazons.update_mobility(game_board)
                ai.make_move(game_board)
                amazons.update_mobility(game_board)
                amazons.set_turn(0)

            elif event.type == pygame.MOUSEBUTTONDOWN:
                amazons.update_mobility(game_board)
                pos = pygame.mouse.get_pos()

                if player_vs_player:
                    x = pos[1] // (HEIGHT + MARGIN)
                    y = pos[0] // (WIDTH + MARGIN)
                    try:
                        if game_board[x][y] == "X":
                            amazons.set_turn(amazons.get_turn() - 1)
                            amazons.clear_illegal(game_board)
                            if amazons.get_turn() == 0:
                                game_board[x][y] = "W"
                            else:
                                game_board[x][y] = "B"
                        else:
                            amazons.move(game_board, x, y)

                    # Player might click on the margin line
                    except IndexError:
                        pass
                else:
                    if amazons.get_turn() < 3:
                        x = pos[1] // (HEIGHT + MARGIN)
                        y = pos[0] // (WIDTH + MARGIN)
                        try:
                            if game_board[x][y] == "X":
                                amazons.set_turn(amazons.get_turn() - 1)
                                amazons.clear_illegal(game_board)
                                game_board[x][y] = "W"
                            else:
                                amazons.move(game_board, x, y)
                        except IndexError:
                            pass

            elif event.type == pygame.MOUSEBUTTONUP:
                amazons.update_mobility(game_board)

        board.draw_board(game_board, WIDTH, HEIGHT, MARGIN,
                         screen, amazons.get_turn(), player_vs_player)

        clock.tick(60)
        pygame.display.flip()

        is_finished(game_board, player_vs_player)


game_intro()
pygame.quit()
quit()
