from __future__ import annotations
from email.utils import parsedate
from typing import Dict

PIECES = []
DJK_MODE = False

class PuzzlePiece:
    def __init__(self, t, r, b, l, idx):
        self.t = t
        self.r = r
        self.b = b
        self.l = l
        self.index = idx

    def __str__(self) -> str:
        return f"{self.index}: {self.t} {self.r} {self.b} {self.l}"

    def get_smallest_side(self):
        return min(self.t, self.r, self.b, self.l)


class PuzzleState:
    def __init__(self, rows, cols, prev_state:PuzzleState=None, x=None, y=None, piece:PuzzlePiece=None):
        self.rows = rows
        self.cols = cols

        if not prev_state:
            self.board = [[None for _ in range(cols)] for _ in range(rows)]
            self.placed_pieces = 0
            self.distance = 0
            self.unused_pieces = PIECES
        else:
            self.board = [[p for p in row] for row in prev_state.board]
            self.board[x][y] = piece
            self.placed_pieces = prev_state.placed_pieces + 1
            self.distance = 1e18
            self.unused_pieces = [p for p in prev_state.unused_pieces if p != piece]

        self.all_pieces = [item for sublist in self.board for item in sublist]

        h = 0
        for piece in self.unused_pieces:
            h += piece.get_smallest_side()

        if not prev_state:
            h -= PIECES[0].get_smallest_side()
    
        self.heuristic = h

        self.hash = hash(tuple(self.all_pieces))
    
    def is_board_empty(self):
        return not bool(self.placed_pieces)

    def get_pieces(self):
        return self.all_pieces

    def get_heuristic(self):
        return self.heuristic

    def get_f_score(self):
        if DJK_MODE:
            return self.distance
        else:
            return self.get_heuristic() + self.distance

    def is_goal_state(self):
        return self.placed_pieces == self.rows * self.cols

    def get_unused_pieces(self):
        return self.unused_pieces

    def get_placement_cost(self, x, y, piece):
        if self.board[x][y]:
            return None, False
        
        valid_edges = []
        if x > 0:
            next_piece = self.board[x-1][y]
            if next_piece and next_piece.b == piece.t:
                valid_edges.append(piece.t)

        if y > 0:
            next_piece = self.board[x][y-1]
            if next_piece and next_piece.r == piece.l:
                valid_edges.append(piece.l)

        if x+1 < self.rows:
            next_piece = self.board[x+1][y]
            if next_piece and next_piece.t == piece.b:
                valid_edges.append(piece.b)

        if y+1 < self.cols:
            next_piece = self.board[x][y+1]
            if next_piece and next_piece.l == piece.r:
                valid_edges.append(piece.r)

        if not valid_edges:
            return None, False
        
        return min(valid_edges), True

    def __eq__(self, other) -> bool:
        return self.hash == other.hash
    
    def __lt__(self, other):
        return self.get_f_score() < other.get_f_score()

    def __str__(self) -> str:
        s = "-------------\n"
        for i in range(self.rows):
            for j in range(self.cols):
                s += f"{'-' if not self.board[i][j] else self.board[i][j].index} "
            s += "\n"
        s += "-------------\n"
        return s
        

class PuzzleGame:
    def __init__(self, rows, cols, pieces, initial_piece):
        self.rows = rows
        self.cols = cols
        self.pieces = pieces
        self.initial_piece = initial_piece
        self.best_state = None
    
    def get_neighbors(self, state: PuzzleState):
        neighbors = []
        if state.is_board_empty():
            for i in range(self.rows):
                for j in range(self.cols):
                    neighbors.append((PuzzleState(self.rows, self.cols, state, i, j, self.initial_piece), 0))
        else:
            unused_pieces = state.get_unused_pieces()
            for piece in unused_pieces:
                for i, row in enumerate(state.board):
                    for j, cell in enumerate(row):
                        if not cell:
                            cost, valid = state.get_placement_cost(i, j, piece)
                            if valid:
                                s = PuzzleState(self.rows, self.cols, state, i, j, piece)
                                neighbors.append((s, cost))

        return neighbors


    def search_solution(self):
        state_list: List[PuzzleState] = [PuzzleState(self.rows, self.cols)]
        explored = []

        counter = 0
        while state_list:
            current_state = min(state_list)
            state_list.remove(current_state)
            explored.append(current_state)
            counter += 1

            if current_state.is_goal_state():
                self.best_state = current_state
                return current_state, counter

            for neighbor, weight in self.get_neighbors(current_state):
                if neighbor in state_list:
                    for a in state_list:
                        if a == neighbor:
                            neighbor.distance = a.distance

                if neighbor in explored:
                    continue
                if current_state.distance + weight < neighbor.distance:
                    if neighbor in state_list:
                        state_list.remove(neighbor)
                    neighbor.distance = current_state.distance + weight
                    state_list.append(neighbor)

        return None


if __name__ == "__main__":
    rows, cols = map(int, input().split())

    PIECES = []
    for i in range(rows*cols):
        t, r, b, l = map(int, input().split())
        PIECES.append(PuzzlePiece(t, r, b, l, i))

    puzzle_game = PuzzleGame(rows, cols, PIECES, PIECES[0])
    puzzle_game.search_solution()
    final_state = puzzle_game.best_state
    print(final_state.get_f_score())