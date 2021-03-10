"""
team game
"""
import arcade

# Constants
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 650
SCREEN_TITLE = "Platformer"

# Size multiplier
CHARACTER_SCALING = 1
TILE_SCALING = 0.5

# Physics constants
PLAYER_MOVEMENT_SPEED = 10
PLAYER_JUMP_SPEED = 25
GRAVITY = 1

# Scroll parameters
LEFT_VIEWPORT_MARGIN = 400
RIGHT_VIEWPORT_MARGIN = 400
BOTTOM_VIEWPORT_MARGIN = 300
TOP_VIEWPORT_MARGIN = 300


class MyGame(arcade.Window):
    """
    Main game window
    """

    def __init__(self):

        # Call the parent class and set up the window
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)

        # initializing map variables
        self.wall_list = None
        self.danger_list = None
        self.environment_list = None
        
        # initializing player variables
        self.player_list = None
        self.player_sprite = None
        self.physics_engine = None

        # initializing scrolling parameters
        self.view_bottom = 0
        self.view_left = 0

        # make sure you start alive
        self.dying = False

        arcade.set_background_color(arcade.csscolor.BLACK)


    def setup(self):
        """ Sets up the game"""
        self.player_list = arcade.SpriteList()        
        
        # sets up the player's character
        image_source = ":resources:images/animated_characters/robot/robot_idle.png"
        self.player_sprite = arcade.Sprite(image_source, CHARACTER_SCALING)
        self.player_sprite.center_x = 600
        self.player_sprite.center_y = 275
        self.player_list.append(self.player_sprite)
        
        # assigns variable to map and map layers
        map_name = "experimental_map.tmx"
        wall_layer_name = "collision_walls"
        dangers_layer_name = "dangers"
        environment_layer_name = "non_collision_walls"
        my_map = arcade.tilemap.read_tmx(map_name)

        # the ground
        self.wall_list = arcade.tilemap.process_layer(map_object=my_map,
                                                        layer_name=wall_layer_name,
                                                        scaling=TILE_SCALING,
                                                        use_spatial_hash=True)

        # the non-iteractable drawings
        self.environment_list = arcade.tilemap.process_layer(my_map, environment_layer_name, TILE_SCALING)

        # the danger areas
        self.danger_list = arcade.tilemap.process_layer(my_map, dangers_layer_name, TILE_SCALING)
 
        # sets up the physics engine
        self.physics_engine = arcade.PhysicsEnginePlatformer(self.player_sprite, self.wall_list, GRAVITY)

    
    def on_draw(self):
        """ Renders the screen. """

        # clear everything on the screen
        arcade.start_render()
        
        # draw everything
        self.environment_list.draw()
        self.wall_list.draw() 
        self.player_list.draw()
        self.danger_list.draw()

        """draw temporary you're dying so that
        he knows that we know that he is supposed
        to die"""
        if self.dying:
            arcade.draw_text("YOU ARE DYING", (self.player_sprite.center_x+50), 
                         self.player_sprite.center_y, arcade.color.RED, 25)


    def on_key_press(self, key, modifiers):
        """updates sprites as key is pressed"""

        if key == arcade.key.UP or key == arcade.key.W:
            if self.physics_engine.can_jump():
                self.player_sprite.change_y = PLAYER_JUMP_SPEED
        elif key == arcade.key.DOWN or key == arcade.key.S:
            self.player_sprite.change_y = -PLAYER_MOVEMENT_SPEED
        elif key == arcade.key.LEFT or key == arcade.key.A:
            self.player_sprite.change_x = -PLAYER_MOVEMENT_SPEED
        elif key == arcade.key.RIGHT or key == arcade.key.D:
            self.player_sprite.change_x = PLAYER_MOVEMENT_SPEED


    def on_key_release(self, key, modifiers):
        """stops updating the sprites when key is released"""

        if key == arcade.key.UP or key == arcade.key.W:
            self.player_sprite.change_y = 0
        elif key == arcade.key.DOWN or key == arcade.key.S:
            self.player_sprite.change_y = 0
        elif key == arcade.key.LEFT or key == arcade.key.A:
            self.player_sprite.change_x = 0
        elif key == arcade.key.RIGHT or key == arcade.key.D:
            self.player_sprite.change_x = 0


    def on_update(self, delta_time):
        """updates the player's position and screen scrolling"""
        
        # moves the player
        self.physics_engine.update()

        # see if the player hit any dangers
        danger_hit_list = arcade.check_for_collision_with_list(self.player_sprite,
                                                               self.danger_list)

        """temporary code to get the screen to print 
        you are dying across the screen. It will
        eventually be replaced with a game over screen"""
        if len(danger_hit_list) > 0:
            self.dying = True
        else:
            self.dying = False

        # the rest manages screen scrolling
        changed = False

        # Scroll left
        left_boundary = self.view_left + LEFT_VIEWPORT_MARGIN
        if self.player_sprite.left < left_boundary:
            self.view_left -= left_boundary - self.player_sprite.left
            changed = True

        # Scroll right
        right_boundary = self.view_left + SCREEN_WIDTH - RIGHT_VIEWPORT_MARGIN
        if self.player_sprite.right > right_boundary:
            self.view_left += self.player_sprite.right - right_boundary
            changed = True

        # Scroll up
        top_boundary = self.view_bottom + SCREEN_HEIGHT - TOP_VIEWPORT_MARGIN
        if self.player_sprite.top > top_boundary:
            self.view_bottom += self.player_sprite.top - top_boundary
            changed = True

        # Scroll down
        bottom_boundary = self.view_bottom + BOTTOM_VIEWPORT_MARGIN
        if self.player_sprite.bottom < bottom_boundary:
            self.view_bottom -= bottom_boundary - self.player_sprite.bottom
            changed = True

        if changed:

            self.view_bottom = int(self.view_bottom)
            self.view_left = int(self.view_left)

            arcade.set_viewport(self.view_left,
                                SCREEN_WIDTH + self.view_left,
                                self.view_bottom,
                                SCREEN_HEIGHT + self.view_bottom)

if __name__ == "__main__":
    window = MyGame()
    window.setup()
    arcade.run()
    arcade.run()
