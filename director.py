import arcade
import math
import os

from introwindows import InstructionView
# Constants
SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 1000
SCREEN_TITLE = "Platformer"



def main():
    """ Main method """

    window = arcade.Window(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    start_view = InstructionView()
    window.show_view(start_view)
    start_view
    arcade.run()


if __name__ == "__main__":
    main()