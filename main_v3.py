from pygame_interface import PygameInterface
from game import new_game


def main():
    interface = PygameInterface(new_game)
    interface.run()


if __name__ == "__main__":
    main()
