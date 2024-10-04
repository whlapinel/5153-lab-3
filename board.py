from domain import IBoard, PositionState


def new_board(width: int, height: int) -> IBoard:
    return Board(width, height)


class Board(IBoard):
    def __init__(self, width=6, depth=7) -> None:
        self.__width = width
        self.__depth = depth
        self.__states_grid: list[list[int]] = [
            [PositionState.PosEmpty.value for pos in range(width)] for _ in range(depth)
        ]
        self.__last_added: tuple[int, int] = (-1, -1)

    def columns(self) -> int:
        return self.__width

    def rows(self) -> int:
        return self.__depth

    def last_added(self) -> tuple[int, int]:
        return self.__last_added

    def accept_move(self, col: int, player: int) -> bool:
        """This will return false if the board is full in that column, true otherwise, and will modify its state accordingly."""
        if self.__states_grid[0][col] != PositionState.PosEmpty.value:
            return False
        for row in range(self.__depth, 0, -1):
            if self.__states_grid[row - 1][col] == PositionState.PosEmpty.value:
                self.__states_grid[row - 1][col] = player
                self.__last_added = (row - 1, col)
                return True
        raise Exception(
            "This should never happen. If the column is full, the first row should have been checked."
        )

    def state(self, row: int, col: int) -> int:
        return self.__states_grid[row][col]

    def states_grid(self):
        return self.__states_grid

    def check_win(self, player: int) -> bool:
        for row in range(self.__depth):
            for col in range(self.__width):
                if self.__states_grid[row][col] == player:
                    if self.__check_win_horizontal(row, col, player):
                        return True
                    if self.__check_win_vertical(row, col, player):
                        return True
                    if self.__check_win_diagonal_down(row, col, player):
                        return True
                    if self.__check_win_diagonal_up(row, col, player):
                        return True
        return False

    def is_full(self) -> bool:
        return all(all(cell != 0 for cell in row) for row in self.states_grid())

    def __check_win_horizontal(self, row: int, col: int, player: int) -> bool:
        if col + 3 >= self.__width:
            return False
        return all(self.__states_grid[row][col + i] == player for i in range(4))

    def __check_win_vertical(self, row: int, col: int, player: int) -> bool:
        if row + 3 >= self.__depth:
            return False
        return all(self.__states_grid[row + i][col] == player for i in range(4))

    def __check_win_diagonal_down(self, row: int, col: int, player: int) -> bool:
        if row + 3 >= self.__depth or col + 3 >= self.__width:
            return False
        return all(self.__states_grid[row + i][col + i] == player for i in range(4))

    def __check_win_diagonal_up(self, row: int, col: int, player: int) -> bool:
        if row + 3 >= self.__depth or col - 3 < 0:
            return False
        return all(
            self.__states_grid[row + i][col - i] == player
            for i in range(
                4,
            )
        )
