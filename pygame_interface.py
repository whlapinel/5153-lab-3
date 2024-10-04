import enum
import math
from typing import Callable
import pygame
import domain

white = (255, 255, 255)
blue = (0, 0, 255)
red = (255, 0, 0)
yellow = (255, 255, 0)
black = (0, 0, 0)


class GameColors(enum.Enum):
    background = black
    p1_piece = yellow
    p2_piece = red
    title_font = white
    instruct_font = white
    col_labels = white
    board = blue


col_key_map = {
    pygame.K_1: 0,
    pygame.K_2: 1,
    pygame.K_3: 2,
    pygame.K_4: 3,
    pygame.K_5: 4,
    pygame.K_6: 5,
    pygame.K_7: 6,
}


class Button:
    def __init__(
        self,
        text: str,
        screen: pygame.Surface,
        pos: tuple[int, int],
        font: pygame.font.Font,
        alignment="center",
    ) -> None:
        self._screen = screen
        self._txt = text
        self._font = font
        self._sfc = font.render(
            self._txt, True, GameColors.title_font.value, GameColors.board.value
        )
        self._pos = pos
        self._rect = pygame.Rect(self._sfc.get_rect(center=self._pos))
        self._rect.inflate_ip(20, 20)
        self._alignment = alignment
        if self._alignment == "left":
            self._rect.bottomleft = self._pos
        else:
            self._rect.center = self._pos

    def render(self):
        pygame.draw.rect(
            self._screen, GameColors.board.value, self._rect, border_radius=20
        )
        text_rect = self._sfc.get_rect(center=self._rect.center)
        self._screen.blit(self._sfc, text_rect)


class Text:
    def __init__(
        self,
        text: str,
        screen: pygame.Surface,
        pos: tuple[int, int],
        font: pygame.font.Font,
        alignment="center",
    ) -> None:
        self._screen = screen
        self._txt = text
        self._font = font
        self._sfc = font.render(self._txt, True, GameColors.title_font.value)
        self._pos = pos
        self._rect = self._sfc.get_rect()
        self._alignment = alignment
        if self._alignment == "left":
            self._rect.bottomleft = self._pos
        else:
            self._rect.center = self._pos

    def render(self):
        pygame.draw.rect(self._screen, GameColors.background.value, self._rect)
        self._sfc = self._font.render(self._txt, True, white)
        self._rect = self._sfc.get_rect()
        if self._alignment == "left":
            self._rect.bottomleft = self._pos
        else:
            self._rect.center = self._pos
        self._screen.blit(self._sfc, self._rect)

    def set_text(self, new_text):
        self._txt = new_text


class PygameInterface:
    def __init__(self, new_game: Callable[[], domain.IGame]) -> None:
        pygame.init()
        self._font = pygame.font.SysFont("Arial", 30)
        self._piece_size = 50
        self._screen = pygame.display.set_mode((1280, 720))
        self._padding = 10  # space between pieces in board
        self._column_width = (self._piece_size) + self._padding  # total width of column
        self._row_height = (self._piece_size) + self._padding  # total height of row
        self._board_width = self._column_width * 7
        self._board_height = self._row_height * 6
        self._board_left = (self._screen.get_width() // 2) - (self._board_width // 2)
        self._board_top = (self._screen.get_height() // 2) - (self._board_height // 2)
        self._board_rect = pygame.Rect(
            self._board_left, self._board_top, self._board_width, self._board_height
        )
        self._game = new_game()
        self._new_game = new_game
        self._board = self._game.board()
        self._clock = pygame.time.Clock()
        self._running = True
        self._timer_start = pygame.time.get_ticks()
        self._timer_complete = False
        self._game_over = False
        self._move_made = False
        self._font = pygame.font.SysFont("Arial", 30)
        self._title = Text(
            "It's player 1's turn",
            self._screen,
            (self._screen.get_width() // 2, 50),
            self._font,
        )
        self._last_move = 0
        self._col_headers: list[Button] = []
        for col in range(self._game.board().columns()):
            pos = (
                self._board_left
                + (self._column_width * col)
                + (self._column_width // 2),
                self._board_top - (self._row_height // 2),
            )
            col_header = Button(
                str(col + 1),
                self._screen,
                pos,
                self._font,
            )
            self._col_headers.append(col_header)
        self._subtitle = Text(
            "Type or click 1-7 to drop your game piece",
            self._screen,
            (self._title._pos[0], self._title._pos[1] + 40),
            self._font,
        )
        self._nodes_explored = Text(
            f"Nodes explored: {self._game.stats().nodes_explored}",
            self._screen,
            (
                self._screen.get_rect().topleft[0] + 40,
                self._screen.get_rect().topleft[1] + 40,
            ),
            self._font,
            alignment="left",
        )
        self._total_nodes = Text(
            f"Total explored: {self._game.stats().total_nodes}",
            self._screen,
            (self._nodes_explored._pos[0], self._nodes_explored._pos[1] + 40),
            self._font,
            alignment="left",
        )
        self._turn_duration = Text(
            f"P2 turn duration: {self._game.stats().turn_duration}",
            self._screen,
            (self._nodes_explored._pos[0], self._nodes_explored._pos[1] + 80),
            self._font,
            alignment="left",
        )
        self._restart_btn = Button(
            "Restart",
            self._screen,
            (self._screen.get_width() // 2 - 60, self._screen.get_height() - 50),
            self._font,
        )
        self._quit_btn = Button(
            "Quit",
            self._screen,
            (self._screen.get_width() // 2 + 60, self._screen.get_height() - 50),
            self._font,
        )
        self._timer_start = pygame.time.get_ticks()
        self.menu_key_map = {pygame.K_q: self.quit, pygame.K_r: self.reset}
        self._buttons = [self._quit_btn, self._restart_btn, *self._col_headers]
        self._game_text = [
            self._title,
            self._subtitle,
            self._nodes_explored,
            self._total_nodes,
            self._turn_duration,
        ]

    def _draw_piece(self, player: int, pos: pygame.Vector2):
        player_colors = {
            0: GameColors.background.value,
            1: GameColors.p1_piece.value,
            2: GameColors.p2_piece.value,
        }
        pygame.draw.circle(
            self._screen,
            player_colors[player],
            (pos + (self._column_width / 2, self._column_width / 2)),
            self._piece_size / 2,
        )

    def _highlight_piece(self, pos: pygame.Vector2):
        pygame.draw.circle(
            self._screen,
            (255, 255, 255),
            (pos + (self._column_width / 2, self._column_width / 2)),
            self._piece_size / 2,
            width=5,
        )

    def reset(self) -> None:
        self._game_over = False
        self._game = self._new_game()
        self._board = self._game.board()
        self._screen.fill((0, 0, 0))
        self._title.set_text("It's player 1's turn")
        self._subtitle.set_text("Enter 1-7 to drop your game piece")

    def _refresh_stats(self):
        self._nodes_explored.set_text(
            f"Nodes explored: {self._game.stats().nodes_explored}"
        )
        self._total_nodes.set_text(f"Total explored: {self._game.stats().total_nodes}")
        duration = round(self._game.stats().turn_duration * 1000, 1)
        self._turn_duration.set_text(f"P2 turn duration: {duration} ms")

    def _player(self):
        return self._game.current_player()

    def _render_board(self):
        pygame.draw.rect(self._screen, GameColors.board.value, self._board_rect)
        grid = self._board.states_grid()
        row_num = 0
        for row in grid:
            col = 0
            for cell in row:
                pos = pygame.Vector2(
                    self._board_left + self._column_width * col,
                    self._board_top + self._row_height * row_num,
                )
                # label columns with numbers 1 - 7
                not_empty = False
                if cell == 1:
                    self._draw_piece(1, pos)
                    not_empty = True
                elif cell == 2:
                    self._draw_piece(2, pos)
                    not_empty = True
                if not_empty:
                    if (row_num, col) == self._board.last_added():
                        self._highlight_piece(pos)
                else:
                    self._draw_piece(0, pos)
                col += 1
            row_num += 1

    def quit(self):
        self._run = False

    def run(self):
        self._run = True
        while self._run:
            # poll for events
            # pygame.QUIT event means the user clicked X to close your window
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self._run = False

                if event.type == pygame.MOUSEBUTTONDOWN and self._player() == 1:
                    if event.button == 1:  # Left mouse button
                        print(f"Mouse clicked! click pos: {event.pos}")
                        if self._quit_btn._rect.collidepoint(event.pos):
                            self.quit()
                        if self._restart_btn._rect.collidepoint(event.pos):
                            self.reset()
                        print(f"length of col headers: {len(self._col_headers)}")
                        for i, header in enumerate(self._col_headers):
                            print(f"header: {header._txt} pos: {header._pos}")
                            if header._rect.collidepoint(event.pos):
                                print(f"header clicked! {header._txt}")
                                self._board.accept_move(i, 1)
                                self._move_made = True
                                self._timer_start = pygame.time.get_ticks()

            keys = pygame.key.get_pressed()
            if not self._game_over:
                if self._move_made:
                    self._move_made = False
                    self._game_over = False
                    player = self._game.next_turn()
                    self._title.set_text(f"It's player {player}'s turn")
                    self._title_text = f"It's player {player}'s turn"
                    self._game.render_CLI()
                if self._game.is_full():
                    print("Board is full!  It's a draw!")
                    self._game_over = True
                for player_num in range(1, 3):
                    if self._board.check_win(player_num):
                        text = f"Player {player_num} wins!"
                        print(text)
                        self._title.set_text(text)
                        self._subtitle.set_text("Press q to quit, r to restart game.")
                        self._game_over = True
                if self._player() == 1:
                    for key, column in col_key_map.items():
                        if keys[key]:
                            self._board.accept_move(col_key_map[key], 1)
                            self._move_made = True
                            self._timer_start = pygame.time.get_ticks()
                elif self._player() == 2:
                    current_time = pygame.time.get_ticks()
                    if current_time - self._timer_start > 200:
                        self._timer_complete = True
                    if self._timer_complete:
                        move = self._game.get_player_input(2)
                        self._board.accept_move(move, 2)
                        self._move_made = True
                        self._timer_complete = False

            else:
                for key, choice in self.menu_key_map.items():
                    if keys[key]:
                        self.menu_key_map[key]()

            self._refresh_stats()
            for text in self._game_text:
                text.render()
            for button in self._buttons:
                button.render()
            self._render_board()
            pygame.display.flip()


pygame.quit()
