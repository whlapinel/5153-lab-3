from board import new_board
from domain import IBoard, IGame, LogEntry
from cli_renderer import new_CLI_renderer
import cpu_player


def new_game() -> IGame:
    return Game()


class Game(IGame):
    def __init__(self) -> None:
        self.__board = new_board(7, 6)
        self.players = 2
        self.p2_human = False
        self.cpu_player = cpu_player.new_cpu_player(self.__board, 2, 1)
        self.__current_player = 1
        self.__renderer = new_CLI_renderer(self.__board)

    def quit(self):
        raise NotImplementedError

    def start(self):
        raise NotImplementedError

    def configure(self, p2_human: bool):
        raise NotImplementedError

    def board(self):
        return self.__board

    def is_full(self) -> bool:
        return self.board().is_full()

    def stats(self) -> LogEntry:
        return self.cpu_player.stats()

    def render_menu(self):
        raise NotImplementedError

    def render_CLI(self):
        self.__renderer.render()

    def next_turn(self) -> int:
        if self.__current_player == 1:
            self.__current_player = 2
        else:
            self.__current_player = 1
        return self.__current_player

    def get_player_input(self, player: int) -> int:
        valid_input_rcvd = False
        input_str = ""
        col = -1
        if player == 2 and self.p2_human == False:
            return self.cpu_player.move()
        else:
            while not valid_input_rcvd:
                input_str = input(
                    f"Player {player}: Select a column (1-7) to place your piece: "
                )
                try:
                    col = int(input_str)
                    if 1 <= col <= 7:
                        valid_input_rcvd = True
                except ValueError:
                    print("Non-integer received - must be an integer.")
            return col - 1

    def current_player(self) -> int:
        return self.__current_player

    def check_win(self, player: int) -> bool:
        return self.__board.check_win(player)
