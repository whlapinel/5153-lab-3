from __future__ import annotations
from abc import ABC, abstractmethod
from enum import Enum
import math
import random
import time
from domain import IBoard, LogEntry
import copy


class GameState:
    def __init__(self, board, curr_player: int, move: int) -> None:
        self.move = move
        """The move (column) that led to this state"""
        self.board: IBoard = board
        self._curr_player = curr_player
        self._children: list[GameState] = []
        self._score = None

    def is_terminal(self):
        """Check if this state is a terminal state (win, loss, or draw)."""
        return (
            self.board.check_win(1) or self.board.check_win(2) or self.board.is_full()
        )

    def generate_children(self) -> list[GameState]:
        children: list[GameState] = []
        next_player = 3 - self._curr_player
        for move in possible_moves(self.board):
            board_copy = copy.deepcopy(self.board)
            board_copy.accept_move(move, self._curr_player)
            child_state = GameState(board_copy, next_player, move)
            children.append(child_state)
        return children

    def switch_players(self):
        if self._curr_player == 1:
            self._curr_player = 2
        else:
            self._curr_player = 1


def new_cpu_player(board: IBoard, player_no: int, opponent: int) -> AIPlayer:
    return AIPlayer(board, player_no, opponent)


class AIPlayer:
    def __init__(self, board: IBoard, player_no: int, opponent: int) -> None:
        self.__board = board
        self.__player_no = player_no
        self.__opponent = opponent
        self.__curr_player = player_no
        self.depth = 3
        self.players = [self.__opponent, self.__player_no]
        self._recurse_count = 0
        self._total_nodes_explored = 0
        self._time_elapsed: float = 0

    def stats(self) -> LogEntry:
        return LogEntry(
            self._recurse_count, self._total_nodes_explored, self._time_elapsed
        )

    def move(self) -> int:
        start = time.perf_counter()
        best_move = random.choice(range(7))
        best_score = -math.inf
        game_state = GameState(self.__board, self.__curr_player, 0)
        children = game_state.generate_children()
        self._recurse_count = 0
        for child in children:
            score = self.minimax(child, self.depth, False, -math.inf, math.inf)
            print("move() score for child: ", score, "move: ", child.move)
            if score > best_score:
                print("Default score has been bested!")
                best_score = score
                best_move = child.move
        print("move() best_move: ", best_move)
        end = time.perf_counter()
        self._time_elapsed = end - start
        self._total_nodes_explored += self._recurse_count
        return best_move

    def minimax(
        self,
        game_state: GameState,
        depth: int,
        maximizing_player: bool,
        alpha: float,
        beta: float,
    ):
        print("minimax() depth: ", depth)
        self._recurse_count += 1
        print("Recurse count: ", self._recurse_count)
        print("game_state.__curr_player: ", game_state._curr_player)
        print("maximizing: ", maximizing_player)
        print("game_state board: ")
        for row in game_state.board.states_grid():
            print(row)
        max_eval = -math.inf
        if depth == 0 or game_state.is_terminal():
            return self.evaluate_board(game_state.board)
        if maximizing_player:
            children = game_state.generate_children()
            for child in children:
                eval = self.minimax(child, depth - 1, False, alpha, beta)
                max_eval = max(max_eval, eval)
                alpha = max(alpha, eval)
                if beta <= alpha:
                    break  # Beta cut-off
            return max_eval
        else:
            min_eval = math.inf
            children = game_state.generate_children()
            for child in children:
                eval = self.minimax(child, depth - 1, True, alpha, beta)
                min_eval = min(min_eval, eval)
                beta = min(beta, eval)
                if beta <= alpha:
                    break  # Alpha cut-off
            return min_eval

    def evaluate_board(self, board: IBoard) -> float:
        score = 0
        close_to_four_self = self.close_to_four_count(self.__player_no, board)
        close_to_four_opp = self.close_to_four_count(self.__opponent, board)
        score += 5 * close_to_four_self
        score -= 5 * close_to_four_opp
        if board.check_win(self.__player_no):
            score += 100
        if board.check_win(self.__opponent):
            score -= 100
        print("score in evaluate_board(): ", score)
        return score

    def close_to_four_count(self, player: int, board: IBoard) -> int:
        """The number of times player has three in a row with a fourth space empty"""
        count = 0
        # Count horizontal instances
        for row in range(board.rows()):
            for col in range(board.columns() - 3):
                if is_close_horiz(row, col, board, player):
                    count += 1
        # Check vertical using same function but passing columns as rows and vice versa
        for col in range(board.columns()):
            for row in range(board.rows() - 3):
                if is_close_vert(row, col, board, player):
                    count += 1
        print("close_to_four_count: ", count)
        return count


def possible_moves(board: IBoard) -> list[int]:
    cols = []
    for col in range(board.columns()):
        if board.state(0, col) == 0:
            cols.append(col)
    return cols


def is_close_horiz(row: int, col: int, board: IBoard, player: int) -> bool:
    """Returns True if the count of `player` for a horizontal window of length 4 starting at `col` is 3 and count of 0 (empty) is 1"""
    window = board.states_grid()[row][col : col + 4]
    has_three_player = window.count(player) == 3
    has_one_empty = window.count(0) == 1
    return has_three_player and has_one_empty


def is_close_vert(row: int, col: int, board: IBoard, player: int) -> bool:
    """Returns True if the count of `player` for a vertical window of length 4 starting at `row` is 3 and count of 0(empty) is 1"""
    column = [rw[col] for rw in board.states_grid()]
    window = column[row : row + 4]
    has_three_player = window.count(player) == 3
    has_one_empty = window.count(0) == 1
    return has_three_player and has_one_empty
