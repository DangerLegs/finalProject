import arcade
import gameview as gv
import os
import math

SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 1000
SCREEN_TITLE = "Platformer"


class Drowned(arcade.View):

    def on_show(self):
        """ This is run once when we switch to this view """
        arcade.set_background_color(arcade.csscolor.DARK_GOLDENROD)
        arcade.set_viewport(0, SCREEN_WIDTH, 0, SCREEN_HEIGHT)
    
    def on_draw(self):
        """ Draw this view """
        arcade.start_render()
        arcade.set_viewport(0, SCREEN_WIDTH, 0, SCREEN_HEIGHT)
        arcade.draw_text("You drowned in the King's poisoned water!", SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2,
                         arcade.color.WHITE, font_size=30, anchor_x="center")
        arcade.draw_text("Click to Try again", SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2-75,
                         arcade.color.WHITE, font_size=20, anchor_x="center")

    def on_mouse_press(self, _x, _y, _button, _modifiers):
        """ If the user presses the mouse button, start the game again. """
        game_view = gv.GameView()
        game_view.setup()
        self.window.show_view(game_view)
