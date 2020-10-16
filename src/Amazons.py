class Amazons:

    def __init__(self):
        self.turn = 0
        self.last_x = 0
        self.last_y = 0
        self.black_wins = 0
        self.white_wins = 0
        self.winner = ""

    def set_params(self, turn, last_x, last_y):
        self.turn = turn
        self.last_x = last_x
        self.last_y = last_y

    def set_winner(self, winner):
        self.winner = winner

    def set_turn(self, turn):
        self.turn = turn

    def get_turn(self):
        return self.turn

    def get_black_wins(self):
        return self.black_wins

    def get_white_wins(self):
        return self.white_wins

    def get_winner(self):
        return self.winner

    def black_won(self):
        self.black_wins += 1

    def white_won(self):
        self.white_wins += 1

    def zero_wins(self):
        self.white_wins = 0
        self.black_wins = 0

    # W stands for white piece, B for black piece, F for fire arrow and X for starting position
    def move(self, board, x, y):
        try:

            # White player's turn
            if board[x][y] == "W" and self.turn == 0:
                if self.cant_move(board, x, y):
                    self.set_params(0, x, y)
                else:
                    board[x][y] = "X"
                    self.set_params(1, x, y)
                    self.display_allowed(board, x, y)

            if board[x][y] == "" and self.turn == 1 and self.allowed(board, self.last_x, self.last_y, x, y):
                board[x][y] = "W"
                self.set_params(2, x, y)
                self.clear_illegal(board)
                self.display_allowed(board, x, y)

            if board[x][y] == "" and self.turn == 2 and self.allowed(board, self.last_x, self.last_y, x, y):
                board[x][y] = "F"
                self.turn = 3
                self.clear_illegal(board)

            # Black player's turn (in player vs. player mode)
            if board[x][y] == "B" and self.turn == 3:
                if self.cant_move(board, x, y):
                    self.set_params(3, x, y)
                else:
                    board[x][y] = "X"
                    self.set_params(4, x, y)
                    self.display_allowed(board, x, y)

            if board[x][y] == "" and self.turn == 4 and self.allowed(board, self.last_x, self.last_y, x, y):
                board[x][y] = "B"
                self.set_params(5, x, y)
                self.clear_illegal(board)
                self.display_allowed(board, x, y)

            if board[x][y] == "" and self.turn == 5 and self.allowed(board, self.last_x, self.last_y, x, y):
                board[x][y] = "F"
                self.turn = 0
                self.clear_illegal(board)

        except IndexError:
            pass

    # Clears illegal positions
    def clear_illegal(self, board):
        for i in range(len(board)):
            for j in range(len(board[0])):
                if board[i][j] == "I" or board[i][j] == "X":
                    board[i][j] = ""

    # Highlights all the squares to which an amazon is able to move
    def display_allowed(self, board, last_x, last_y):
        for i in range(len(board)):
            for j in range(len(board[0])):
                if not self.allowed(board, last_x, last_y, i, j):
                    if board[i][j] == "":
                        board[i][j] = "I"

    # Determines to which positions an amazon is able to move
    def allowed(self, board, x1, y1, x2, y2):
        if x1 == x2 or y1 == y2 or abs(x1 - x2) == abs(y1 - y2):
            j = 0
            if x2 < x1 and y2 < y1:
                for i in range(x2 + 1, x1):
                    j += 1
                    if board[i][y2 + j] != "":
                        return False

            if x2 < x1 and y2 > y1:
                for i in range(x2 + 1, x1):
                    j += 1
                    if board[i][y2 - j] != "":
                        return False

            if x2 < x1 and y2 == y1:
                for i in range(x2 + 1, x1):
                    if board[i][y1] != "":
                        return False

            if x2 > x1 and y2 == y1:
                for i in range(x1 + 1, x2):
                    if board[i][y1] != "":
                        return False

            if x2 > x1 and y2 < y1:
                for i in range(x1 + 1, x2):
                    j += 1
                    if board[i][y1 - j] != "":
                        return False

            if x2 > x1 and y2 > y1:
                for i in range(x1 + 1, x2):
                    j += 1
                    if board[i][y1 + j] != "":
                        return False

            if x2 == x1 and y2 < y1:
                for i in range(y2 + 1, y1):
                    if board[x1][i] != "":
                        return False

            if x2 == x1 and y2 > y1:
                for i in range(y1 + 1, y2):
                    if board[x1][i] != "":
                        return False
            return True
        else:
            return False

    # Checks if an amazon is stuck
    def cant_move(self, board, x, y):
        moves = 0
        illegals = 0
        neighbours = [(x - 1, y - 1), (x, y - 1), (x + 1, y - 1),
                      (x - 1, y),                 (x + 1, y),
                      (x - 1, y + 1), (x, y + 1), (x + 1, y + 1)]

        for x, y in neighbours:
            if x >= 0 and y >= 0:
                try:
                    moves += 1
                    if board[x][y] != "" and board[x][y] != "I":
                        illegals += 1
                except IndexError:
                    moves -= 1
                    pass

        if moves == illegals:
            return True
        else:
            return False

    # Checks if an amazon is able to move [determines if an amazon is dead (DW or DB) or alive]
    def update_mobility(self, board):
        for i in range(len(board)):
            for j in range(len(board[0])):
                if board[i][j] == "W" and self.cant_move(board, i, j):
                    board[i][j] = "DW"
                if board[i][j] == "DW" and not self.cant_move(board, i, j):
                    board[i][j] = "W"
                if board[i][j] == "B" and self.cant_move(board, i, j):
                    board[i][j] = "DB"
                if board[i][j] == "DB" and not self.cant_move(board, i, j):
                    board[i][j] = "B"

    # Ends the game and determines the winner
    def finished(self, board):
        whites = 0
        blacks = 0
        temporary = 0

        for i in range(len(board)):
            for j in range(len(board[0])):
                if board[i][j] == "W":
                    whites += 1
                if board[i][j] == "B":
                    blacks += 1
                if board[i][j] == "X":
                    temporary += 1

        if whites == 0 and temporary == 0:
            self.set_winner("Black")
            return True
        if blacks == 0 and temporary == 0:
            self.set_winner("White")
            return True
