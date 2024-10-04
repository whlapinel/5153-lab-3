from abc import ABC, abstractmethod
from enum import Enum


class PositionState(Enum):
    PosEmpty = 0
    Player1 = 1
    Player2 = 2


class LogEntry:
    def __init__(self, nodes_explored, total_nodes, turn_duration) -> None:
        self.nodes_explored = nodes_explored
        self.total_nodes = total_nodes
        self.turn_duration = turn_duration


class IBoard(ABC):
    @abstractmethod
    def accept_move(self, col: int, player: int) -> bool:
        """This will return false if the board is full in that column, true otherwise, and will modify its state accordingly."""

    @abstractmethod
    def state(self, row: int, col: int) -> int:
        """This will return the state of a given position on the board, either empty or Player1, or Player2, the latter two indicating a piece is in the position"""

    @abstractmethod
    def states_grid(self) -> list[list[int]]:
        """This will return the entire board state"""

    @abstractmethod
    def check_win(self, player: int) -> bool:
        """This will check if the player has won the game"""

    @abstractmethod
    def columns(self) -> int:
        """Returns column count for ranging over"""

    @abstractmethod
    def rows(self) -> int:
        """Return row count for ranging over"""

    @abstractmethod
    def is_full(self) -> bool:
        """Returns true if no spaces remain on board, false otherwise"""

    @abstractmethod
    def last_added(self) -> tuple[int, int]:
        """Returns the cell of the last piece added"""


class IGame(ABC):
    @abstractmethod
    def quit(self):
        """This allows a user to quit the game."""

    @abstractmethod
    def start(self):
        """This allows a user to start the game."""

    @abstractmethod
    def configure(self, p2_human: bool):
        """This allows a user to configure the game"""

    def render_menu(self):
        """This will render the menu for the game"""

    @abstractmethod
    def render_CLI(self):
        """This will render the game state"""

    @abstractmethod
    def next_turn(self) -> int:
        """This will allow the next turn to be played"""

    @abstractmethod
    def get_player_input(self, player: int) -> int:
        """This will get the player input"""

    @abstractmethod
    def board(self) -> IBoard:
        """This will return the board"""

    @abstractmethod
    def is_full(self) -> bool:
        """Returns true when board is full"""

    @abstractmethod
    def current_player(self) -> int:
        """This will return the current player"""

    @abstractmethod
    def stats(self) -> LogEntry:
        """This returns a multi-line string with all the required stats"""


class IRenderer(ABC):
    @abstractmethod
    def render(self):
        """This will render the game state"""
