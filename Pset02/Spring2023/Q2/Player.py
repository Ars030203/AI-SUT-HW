from Board import BoardUtility
import math
import random


ROWS = 6
COLS = 6
ROTATES = ["skip", "clockwise", "anticlockwise"]
AREAS = [1, 2, 3, 4]

class Player:
    def __init__(self, token):
        self.token = token

    def perform_move(self, game_board):
        return 0

class RandomPlayer(Player):
    def perform_move(self, game_board):
        return [random.choice(BoardUtil.get_valid_positions(game_board)),
                random.choice(AREAS),
                random.choice(ROTATES)]

class HumanPlayer(Player):
    def perform_move(self, game_board):
        move_input = input("Enter row, col, area, and rotation (separated by spaces):\n")
        move_parts = move_input.split()
        return [[int(move_parts[0]), int(move_parts[1])], int(move_parts[2]), move_parts[3]]

class Scoring:
    @staticmethod
    def count_borders(board, token):
        border_count = 0

        for c in range(COLS):
            if board[0][c] == token or board[ROWS-1][c] == token:
                border_count += 1

        for r in range(ROWS):
            if board[r][0] == token or board[r][COLS-1] == token:
                border_count += 1

        return border_count

    # The rest of the Scoring class remains unchanged

class MaxiMinPlayer(Player):
    def __init__(self, token, depth=5):
        super().__init__(token)
        self.depth = depth

    @staticmethod
    def minimax_algo(board, depth, token, alpha, beta, is_maximizer):
        if BoardUtil.is_terminal_state(board) or depth == 0:
            return Scoring.get_position_score(board, token), None

        value = -100_000_000_000 if is_maximizer == 1 else 100_000_000_000
        positions = BoardUtil.get_valid_positions(board)
        move = [positions[0], 1, 'skip']
        next_token = 1 if token == 2 else 1

        high_value_choices = []

        for [row, col], area, rotation in zip(positions, AREAS, ROTATES):
            copied_board = board.copy()
            BoardUtil.make_move(copied_board, row, col, area, rotation, token)
            new_value, _ = MaxiMinPlayer.minimax_algo(copied_board, depth-1, next_token, alpha, beta, is_maximizer * -1)
            
            if is_maximizer == 1:
                if new_value > beta:
                    break
                if new_value > value:
                    value = new_value
                    move = [[row, col], area, rotation]
                alpha = max(alpha, value)
                high_value_choices.append([value, move])
            else:
                if new_value < alpha:
                    break
                if new_value < value:
                    value = new_value
                    move = [[row, col], area, rotation]
                beta = min(beta, value)

        if is_maximizer == 1 and random.random() <= 0.1:  # Probability of 0.1
            return random.choice(high_value_choices)

        return value, move

    def perform_move(self, board):
        _, move = MaxiMinPlayer.minimax_algo(board, self.depth, self.token, -math.inf, math.inf, 1)
        return move