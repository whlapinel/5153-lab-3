from domain import IRenderer, IBoard


class PlayerChars:
    Player1 = "X"
    Player2 = "O"
    Empty = " "


def new_CLI_renderer(board: IBoard) -> IRenderer:
    return CLIRenderer(board)


class CLIRenderer(IRenderer):
    def __init__(self, board: IBoard) -> None:
        self.__board = board

    def render(self):
        states = self.__board.states_grid()
        for row in states:
            print("|", end="")
            for state in row:
                if state == 1:
                    print(PlayerChars.Player1, end="|")
                elif state == 2:
                    print(PlayerChars.Player2, end="|")
                else:
                    print(PlayerChars.Empty, end="|")
            print()
