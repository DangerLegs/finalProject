import arcade
import math
import os

from gameview import GameView


# Constants
SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 1000
SCREEN_TITLE = "Platformer"


# Instruction screen / main menu
class InstructionView(arcade.View):

    def on_show(self):
        """ This is run once when we switch to this view """
        arcade.set_background_color(arcade.csscolor.DARK_GOLDENROD)
        arcade.set_viewport(0, SCREEN_WIDTH - 1, 0, SCREEN_HEIGHT - 1)
    
    def on_draw(self):
        """ Draw this view """
        arcade.start_render()
        arcade.draw_text("""Use the w key or up on the key pad to jump. Use the 'a' and 'd' keys 
        or the left and right arrows on the key pad to move left or right.
        Don't hit the enemies or you'll die.""", SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2,
                         arcade.color.WHITE, font_size=50, anchor_x="center")
        arcade.draw_text("Click to advance", SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2-75,
                         arcade.color.WHITE, font_size=20, anchor_x="center")

    def on_mouse_press(self, _x, _y, _button, _modifiers):
        """ If the user presses the mouse button, start the game. """
        game_view = IntroView()
        game_view
        self.window.show_view(game_view)

# Intro screen that tells the protagonists story 
class IntroView(arcade.View):

    def on_show(self):
        """ This is run once when we switch to this view """
        arcade.set_background_color(arcade.csscolor.DARK_GOLDENROD)
        arcade.set_viewport(0, SCREEN_WIDTH - 1, 0, SCREEN_HEIGHT - 1)
    
    def on_draw(self):
        """ Draw this view """
        arcade.start_render()
    arcade.draw_text("""                                 

                                    Oh no! King Dino is on a rampage!

                The town is going to be reduced to rubble if he's not stopped!

                His water was poisened his water and turned him into a savage beast!

                There is only one special potion that can make it pure again.

                                    You are the only one who can help him. 


            Do you have what it takes to overcome the sinister 
            forces that stand in your way and save the King?
                                                              """, SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2,
                             arcade.color.WHITE, font_size=20, anchor_x="center")
            arcade.draw_text("Proceed if you dare! (Click to advance)", SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2-75,
                             arcade.color.WHITE, font_size=20, anchor_x="center")

    def on_mouse_press(self, _x, _y, _button, _modifiers):
        """ If the user presses the mouse button, start the game. """
        game_view = GameView()
        game_view.setup()
        self.window.show_view(game_view)


