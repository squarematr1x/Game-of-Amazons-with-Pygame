import random
from collections import defaultdict
from Amazons import Amazons


class AI:

    def __init__(self):
        self.first_position = True
        self.moved = False
        self.x = 0
        self.y = 0
        self.future_x = 0
        self.future_y = 0
        self.final_x = 0
        self.final_y = 0
        self.arrow_x = 0
        self.arrow_y = 0
        self.evaluations = 275

    def set_first_position(self, boolean):
        self.first_position = boolean

    def set_moved(self, boolean):
        self.moved = boolean

    def set_pos(self, x, y):
        self.x = x
        self.y = y

    def set_future_pos(self):
        if not self.moved:
            self.future_x = random.randint(0, 9)
            self.future_y = random.randint(0, 9)

    def set_arrow(self):
        self.arrow_x = random.randint(0, 9)
        self.arrow_y = random.randint(0, 9)

    def get_pos(self):
        return self.x, self.y

    def get_future_pos(self):
        return self.future_x, self.future_y

    def get_arrow_pos(self):
        return self.arrow_x, self.arrow_y

    # Choosing random black amazon from the game board
    def find_black(self, board):
        black_amazons = defaultdict(list)
        available_black_amazons = defaultdict(list)
        black_keys = []
        available_black_keys = []
        chosen_x = 0
        chosen_y = 0
        not_stuck = False

        if self.first_position:
            for i in range(len(board)):
                for j in range(len(board[0])):
                    if board[i][j] == "B":
                        black_amazons[i].append(j)

            for key in black_amazons.keys():
                black_keys.append(key)

            for x, y in black_amazons.items():
                try:
                    if self.count_empty(board, x, y[0]) < 3 and self.count_allowed(board, x, y[0]) > 2:
                        chosen_x = x
                        chosen_y = y[0]
                    elif self.count_empty(board, x, y[1]) < 3 and self.count_allowed(board, x, y[1]) > 2:
                        chosen_x = x
                        chosen_y = y[1]
                    else:
                        if self.count_allowed(board, x, y[1]) > 3:
                            available_black_amazons[x].append(y[1])
                            not_stuck = True

                except IndexError:
                    pass

            for key in available_black_amazons.keys():
                available_black_keys.append(key)

            if chosen_x == 0 and chosen_y == 0:
                if not_stuck:
                    x = random.choice(available_black_keys)
                    y = random.choice(available_black_amazons[x])
                else:
                    x = random.choice(black_keys)
                    y = random.choice(black_amazons[x])
            else:
                x, y = chosen_x, chosen_y

            self.set_pos(x, y)
            self.set_first_position(False)
            self.set_moved(False)

    def count_allowed(self, board, x, y):
        amazons = Amazons()
        score = 0
        for i in range(len(board)):
            for j in range(len(board[0])):
                if board[i][j] == "" and amazons.allowed(board, x, y, i, j):
                    score += 1
        return score

    def count_empty(self, board, x, y):
        moves = 0
        neighbours = [(x - 1, y - 1), (x, y - 1), (x + 1, y - 1),
                      (x - 1, y),                 (x + 1, y),
                      (x - 1, y + 1), (x, y + 1), (x + 1, y + 1)]

        for x, y in neighbours:
            if x >= 0 and y >= 0:
                try:
                    if board[x][y] == "":
                        moves += 1
                except IndexError:
                    pass
        return moves

    def new_move(self, board, color):
        amazons = Amazons()
        self.find_black(board)

        while not self.moved:
            self.set_future_pos()

            if board[self.future_x][self.future_y] == "" and \
                    amazons.allowed(board, self.x, self.y, self.future_x, self.future_y):
                board[self.future_x][self.future_y] = color
                board[self.x][self.y] = ""
                self.set_moved(True)
                self.set_first_position(True)

    def fire(self, board):
        amazons = Amazons()
        arrow_shot = False

        while not arrow_shot:
            self.set_arrow()
            if board[self.arrow_x][self.arrow_y] == "" and \
                    amazons.allowed(board, self.final_x, self.final_y, self.arrow_x, self.arrow_y):
                board[self.arrow_x][self.arrow_y] = "F"
                arrow_shot = True

    def undo_move(self, board, move):
        for i in range(len(board)):
            for j in range(len(board[0])):
                if move == "B":
                    if (i, j) == self.get_future_pos():
                        board[i][j] = ""
                    if (i, j) == self.get_pos():
                        board[i][j] = "B"
                if move == "F":
                    if (i, j) == self.get_arrow_pos():
                        board[i][j] = ""


    def find_amazon_coordinates(self, board, amazon_color):
        amazons = defaultdict(list)
        for i in range(len(board)):
            for j in range(len(board[0])):
                if board[i][j] == amazon_color:
                    amazons[i].append(j)
        return amazons

    def amazon_mobility(self, board, amazon_color):
        amazons = Amazons()
        copy_board = [[0 for x in range(10)] for y in range(10)]
        amazons_coordinates = self.find_amazon_coordinates(board, amazon_color)
        score = 0

        for x, y in amazons_coordinates.items():
            for i in range(len(board)):
                for j in range(len(board[0])):
                    try:
                        if board[i][j] == "" and amazons.allowed(board, x, y[0], i, j) and copy_board[i][j] == 0:
                            copy_board[i][j] = 1
                            score += 1
                        if board[i][j] == "" and amazons.allowed(board, x, y[1], i, j) and copy_board[i][j] == 0:
                            copy_board[i][j] = 1
                            score += 1
                    except IndexError:
                        pass
        return score

    # If this method returns a positive integer, then black amazon has better mobility than white
    def evaluate_mobility(self, board):
        return self.amazon_mobility(board, "B") - self.amazon_mobility(board, "W")

    def next_coordinates(self, board, amazon_color):
        amazons = Amazons()
        score_board = [[0 for x in range(10)] for y in range(10)]

        coordinates = self.find_amazon_coordinates(board, amazon_color)
        moves = defaultdict(list)
        max_eval = 4

        for territory in range(1, max_eval):
            for x, y in coordinates.items():
                for i in range(len(board)):
                    for j in range(len(board[0])):
                        try:
                            if board[i][j] == "" and amazons.allowed(board, x, y[0], i, j):
                                if score_board[i][j] == 0:
                                    score_board[i][j] = territory
                                    moves[i].append(j)
                            if board[i][j] == "" and amazons.allowed(board, x, y[1], i, j):
                                if score_board[i][j] == 0:
                                    score_board[i][j] = territory
                                    moves[i].append(j)
                        except IndexError:
                            pass

            coordinates.clear()
            coordinates = moves.copy()
            moves.clear()

        return score_board

    # Defines who owns each square
    def evaluate_territory(self, board):
        white_territory = self.next_coordinates(board, "W")
        black_territory = self.next_coordinates(board, "B")

        black_score = 0
        white_score = 0

        for i in range(len(board)):
            for j in range(len(board[0])):
                if white_territory[i][j] > black_territory[i][j]:
                    black_score += 1
                if white_territory[i][j] < black_territory[i][j]:
                    white_score += 1

        return black_score - white_score

    def copy_game_board(self, board1, board2):
        for i in range(len(board1)):
            for j in range(len(board1)):
                board1[i][j] = board2[i][j]

    def best_move(self, board):
        final_board = [[0 for x in range(10)] for y in range(10)]
        best_board_value = -999

        for i in range(0, self.evaluations):
            self.new_move(board, "B")
            new_board_value = self.evaluate_mobility(board) + (self.evaluate_territory(board) * 2)

            if new_board_value > best_board_value:
                self.final_x, self.final_y = self.future_x, self.future_y
                best_board_value = new_board_value
                self.copy_game_board(final_board, board)

            self.undo_move(board, "B")

        self.copy_game_board(board, final_board)

    def best_shot(self, board):
        final_board = [[0 for x in range(10)] for y in range(10)]
        best_board_value = -999

        for i in range(0, self.evaluations):
            self.fire(board)
            if self.count_empty(board, self.final_x, self.final_y) < 3:
                new_board_value = self.evaluate_mobility(board)
            else:
                new_board_value = self.evaluate_mobility(board) + self.evaluate_territory(board)

            if new_board_value > best_board_value:
                best_board_value = new_board_value
                self.copy_game_board(final_board, board)

            self.undo_move(board, "F")

        self.copy_game_board(board, final_board)

    def make_move(self, board):
        self.best_move(board)
        self.best_shot(board)
