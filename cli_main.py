import os
from game import new_game


if __name__ == "__main__":

    game = new_game()
    player = game.current_player()
    while True:
        game.render_CLI()
        col = game.get_player_input(player)
        # os.system("clear")
        if game.board().accept_move(col, player):
            if game.board().check_win(player):
                game.render_CLI()
                print(f"Player {player} wins!")
                break
            player = game.next_turn()
            if game.is_full():
                print("It's a draw!")
                break
        else:
            print("Move not acceptable!")
