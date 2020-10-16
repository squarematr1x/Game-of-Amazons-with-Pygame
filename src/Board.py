import pygame


class Board:

    def __init__(self):
        self.board = [[0 for x in range(10)] for y in range(10)]
        self.fire = pygame.image.load(r'pictures/fire_arrow.png')
        self.black = pygame.image.load(r'pictures/black_piece.png')
        self.white = pygame.image.load(r'pictures/white_piece.png')
        self.dead_white = pygame.image.load(r'pictures/dead_white_piece.png')
        self.dead_black = pygame.image.load(r'pictures/dead_black_piece.png')
        self.first_move = pygame.image.load(r'pictures/first_move.png')
        self.board_col1 = (190, 160, 160)
        self.board_col2 = (225, 204, 153)
        self.board_col3 = (126, 96, 96)
        self.board_col4 = (204, 102, 0)

    def get_board(self):
        return self.board

    @staticmethod
    def initialize_board(board):
        for i in range(len(board)):
            for j in range(len(board[0])):
                if j == (len(board[0]) // 2) + 1 or j == (len(board[0]) // 2) - 2:
                    if i == 0:
                        board[i][j] = "B"
                    elif i == len(board) - 1:
                        board[i][j] = "W"
                    else:
                        board[i][j] = ""
                elif j == 0 or j == len(board[0]) - 1:
                    if i == len(board) // 2 - 2:
                        board[i][j] = "B"
                    elif i == len(board) // 2 + 1:
                        board[i][j] = "W"
                    else:
                        board[i][j] = ""
                else:
                    board[i][j] = ""

    # Check if current board has illegal positions
    @staticmethod
    def illegals(board, width, height):
        illegals = 0
        for i in range(width // 5):
            for j in range(height // 5):
                if (i + j) % 2 == 0 and board[i][j] == "I":
                    illegals += 1
                    break
        return illegals

    def draw_objects(self, board, width, height, margin, screen, turn, player_vs_player):
        for i in range(width // 5):
            for j in range(height // 5):
                if board[i][j] == "F":
                    screen.blit(self.fire, [(margin + width) * j + margin,
                                            (margin + height) * i + margin, width, height])
                if board[i][j] == "W":
                    if turn == 0:
                        screen.blit(self.first_move, [(margin + width) * j + margin,
                                                      (margin + height) * i + margin, width, height])
                    screen.blit(self.white, [(margin + width) * j + margin,
                                             (margin + height) * i + margin, width, height])
                if board[i][j] == "B":
                    if turn == 3 and player_vs_player:
                        screen.blit(self.first_move, [(margin + width) * j + margin,
                                                      (margin + height) * i + margin, width, height])
                    screen.blit(self.black, [(margin + width) * j + margin,
                                             (margin + height) * i + margin, width, height])
                if board[i][j] == "DW":
                    screen.blit(self.dead_white, [(margin + width) * j + margin,
                                                  (margin + height) * i + margin, width, height])
                if board[i][j] == "DB":
                    screen.blit(self.dead_black, [(margin + width) * j + margin,
                                                  (margin + height) * i + margin, width, height])
                if board[i][j] == "X":
                    screen.blit(self.first_move, [(margin + width) * j + margin,
                                                  (margin + height) * i + margin, width, height])

    def draw_board(self, board, width, height, margin, screen, turn, player_vs_player):
        for i in range(width // 5):
            for j in range(height // 5):
                if (i + j) % 2 == 0:
                    if board[i][j] != "" and self.illegals(board, width, height) > 0:
                        color = self.board_col1
                    else:
                        color = self.board_col2
                else:
                    if board[i][j] != "" and self.illegals(board, width, height) > 0:
                        color = self.board_col3
                    else:
                        color = self.board_col4

                pygame.draw.rect(screen, color, [(margin + width) * j + margin,
                                                 (margin + height) * i + margin, width, height])
        self.draw_objects(board, width, height, margin, screen, turn, player_vs_player)
