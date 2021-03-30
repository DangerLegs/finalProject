import arcade
import os
import math
from protagonist import PlayerCharacter
from boss import BossCharacter
from enemy import EnemyCharacter

"""HERE WE DECLARE OUR CONSTANTS"""

# Screen dimensions
SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 1000
SCREEN_TITLE = "Platformer"

# Constants used to scale our sprites from their original size
TILE_SCALING = 0.25
SPRITE_PIXEL_SIZE = 150
GRID_PIXEL_SIZE = (SPRITE_PIXEL_SIZE * TILE_SCALING)
POTION_SCALING = 10

# Movement speed of player, in pixels per frame
PLAYER_MOVEMENT_SPEED = 9
GRAVITY = 1.3
PLAYER_JUMP_SPEED = 25
# movement speed of enemies
ENEMY_MOVEMENT_SPEED = 3
BOSS_MOVEMENT_SPEED = -7
POTION_MOVEMENT_SPEED = 0
# How many pixels to keep as a minimum margin between the character
# and the edge of the screen.
LEFT_VIEWPORT_MARGIN = 500
RIGHT_VIEWPORT_MARGIN = 500
BOTTOM_VIEWPORT_MARGIN = 400
TOP_VIEWPORT_MARGIN = 400
# More scaling constants
PLAYER_START_X = SPRITE_PIXEL_SIZE * TILE_SCALING * 2
PLAYER_START_Y = SPRITE_PIXEL_SIZE * TILE_SCALING * 1


class GameView(arcade.View):
    """
    Main application class.
    """

    def __init__(self):
        """
        Initializer for the game
        """

        # Call the parent class and set up the window
        super().__init__()

        # Set the path to start with this program
        file_path = os.path.dirname(os.path.abspath(__file__))
        os.chdir(file_path)

        # Track the current state of what key is pressed
        self.left_pressed = False
        self.right_pressed = False
        self.up_pressed = False
        self.down_pressed = False
        self.jump_needs_reset = False

        # These are 'lists' that keep track of our sprites. Each sprite should
        # go into a list.
        self.wall_list = None
        self.background_list = None
        self.player_list = None
        self.ememy_list = None
        self.potion_list = None


        # Separate variable that holds the player sprite
        self.player_sprite = None


        # do we have the potion
        self.has_potion = False

        # Our 'physics' engine
        self.physics_engine = None

        # enemy physics engine
        self.boss_physics_engine = None
        self.enemy_sprite_2_physics_engine = None
        self.enemy_sprite_3_physics_engine = None
        self.enemy_sprie_4_physics_engine = None
        self.potion_sprite_physics_engine = None

        # Used to keep track of our scrolling
        self.view_bottom = 0
        self.view_left = 0

        self.end_of_map = 0

        # Keep track of the lives
        self.lives = 1
        if self.lives == 0:
                end = GameOverView()
                end

        

        # Load sounds
        self.collect_coin_sound = arcade.load_sound(":resources:sounds/coin1.wav")
        self.jump_sound = arcade.load_sound(":resources:sounds/jump1.wav")
        self.game_over = arcade.load_sound(":resources:sounds/gameover1.wav")

    def setup(self):
        """ Set up the game here. Call this function to restart the game. """

        
        # Used to keep track of our scrolling
        self.view_bottom = 0
        self.view_left = 0

        # Keep track of the lives
        self.lives = 1
        if self.lives == 0:
                end = GameOverView()
                end

        # Create the Sprite lists
        self.player_list = arcade.SpriteList()
        self.wall_list = arcade.SpriteList()
        self.enemy_list = arcade.SpriteList()

        # Set up the player, specifically placing it at these coordinates.
        self.player_sprite = PlayerCharacter()
        self.player_sprite.center_x = PLAYER_START_X
        self.player_sprite.center_y = PLAYER_START_Y
        self.player_list.append(self.player_sprite)

        # Set up the boss
        self.boss_sprite = BossCharacter()
        self.boss_sprite.center_x = 3080
        self.boss_sprite.center_y = 1573
        self.enemy_list.append(self.boss_sprite)
        
        # set up the enemies
        self.enemy_sprite_2 = EnemyCharacter()
        self.enemy_sprite_2.center_x = 520
        self.enemy_sprite_2.center_y = 965
        self.enemy_list.append(self.enemy_sprite_2)
        self.enemy_sprite_3 = EnemyCharacter()
        self.enemy_sprite_3.center_x = 1060
        self.enemy_sprite_3.center_y = 1637   
        self.enemy_list.append(self.enemy_sprite_3)
        self.enemy_sprite_4 = EnemyCharacter()
        self.enemy_sprite_4.center_x = 160
        self.enemy_sprite_4.center_y = 2084                
        self.enemy_list.append(self.enemy_sprite_4)
        
        #setup potion pick up sprite
        self.potion_list = arcade.SpriteList()
        potion_image_source = "Documentation/angry_dino_idle.png"
        self.potion_sprite = arcade.Sprite(potion_image_source, POTION_SCALING)
        self.potion_sprite.center_x = 3128
        self.potion_sprite.center_y = 1024
        self.potion_list.append(self.potion_sprite)

        # Map name
        map_name = 'Documentation/game_map_1.tmx'
        
        # Name of the layer in the file that has our platforms/walls
        wall_layer_name = "collision_blocks"
        dangers_layer_name = "danger_blocks"

        # Read in the tiled map
        my_map = arcade.tilemap.read_tmx(map_name)

        # Calculate the right edge of the my_map in pixels
        self.end_of_map = my_map.map_size.width * GRID_PIXEL_SIZE

        # -- Platforms
        self.wall_list = arcade.tilemap.process_layer(map_object=my_map,
                                                        layer_name=wall_layer_name,
                                                        scaling=TILE_SCALING,
                                                        use_spatial_hash=True)

        # --- Other stuff
        # Set the background color
        if my_map.background_color:
            arcade.set_background_color(my_map.background_color)
            
        # the danger areas
        self.danger_list = arcade.tilemap.process_layer(my_map, dangers_layer_name, TILE_SCALING)
 
       
        # Create the 'physics engine'
        self.physics_engine = arcade.PhysicsEnginePlatformer(self.player_sprite,
                                                             self.wall_list,
                                                             gravity_constant=GRAVITY)
        
        self.boss_physics_engine = arcade.PhysicsEnginePlatformer(self.boss_sprite,
                                                             self.wall_list,
                                                             gravity_constant=GRAVITY)

        self.enemy2_physics_engine = arcade.PhysicsEnginePlatformer(self.enemy_sprite_2,
                                                             self.wall_list,
                                                             gravity_constant=GRAVITY)

        self.enemy3_physics_engine = arcade.PhysicsEnginePlatformer(self.enemy_sprite_3,
                                                             self.wall_list,
                                                             gravity_constant=GRAVITY)

        self.enemy4_physics_engine = arcade.PhysicsEnginePlatformer(self.enemy_sprite_4,
                                                             self.wall_list,
                                                             gravity_constant=GRAVITY)

        self.potion_sprite_physics_engine = arcade.PhysicsEnginePlatformer(self.potion_sprite,
                                                            self.wall_list,
                                                            gravity_constant=GRAVITY)                                                     

    def on_draw(self):
        """ Render the screen. """

        # Clear the screen to the background color
        arcade.start_render()

        # Draw our sprites
        self.wall_list.draw()
        self.player_list.draw()
        self.enemy_list.draw()
        self.potion_sprite.draw()

        # Draw our score on the screen, scrolling it with the viewport
        lives_text = f"Lives: {self.lives}"
        arcade.draw_text(lives_text, 10 + self.view_left, 10 + self.view_bottom,
                         arcade.csscolor.BLACK, 18)

        # self.player_sprite.draw_hit_box(arcade.color.RED, 3)

    def process_keychange(self):
        """
        Called when we change a key up/down or we move on/off a ladder.
        """
        # Process up/down
        if self.up_pressed and not self.down_pressed:
            if self.physics_engine.is_on_ladder():
                self.player_sprite.change_y = PLAYER_MOVEMENT_SPEED
            elif self.physics_engine.can_jump(y_distance=10) and not self.jump_needs_reset:
                self.player_sprite.change_y = PLAYER_JUMP_SPEED
                self.jump_needs_reset = True
                # arcade.play_sound(self.jump_sound)
        elif self.down_pressed and not self.up_pressed:
            if self.physics_engine.is_on_ladder():
                self.player_sprite.change_y = -PLAYER_MOVEMENT_SPEED

        # Process left/right
        if self.right_pressed and not self.left_pressed:
            self.player_sprite.change_x = PLAYER_MOVEMENT_SPEED
        elif self.left_pressed and not self.right_pressed:
            self.player_sprite.change_x = -PLAYER_MOVEMENT_SPEED
        else:
            self.player_sprite.change_x = 0

    def on_key_press(self, key, modifiers):
        """Called whenever a key is pressed. """

        if key == arcade.key.UP or key == arcade.key.W:
            self.up_pressed = True
        elif key == arcade.key.DOWN or key == arcade.key.S:
            self.down_pressed = True
        elif key == arcade.key.LEFT or key == arcade.key.A:
            self.left_pressed = True
        elif key == arcade.key.RIGHT or key == arcade.key.D:
            self.right_pressed = True

        self.process_keychange()

    def on_key_release(self, key, modifiers):
        """Called when the user releases a key. """

        if key == arcade.key.UP or key == arcade.key.W:
            self.up_pressed = False
            self.jump_needs_reset = False
        elif key == arcade.key.DOWN or key == arcade.key.S:
            self.down_pressed = False
        elif key == arcade.key.LEFT or key == arcade.key.A:
            self.left_pressed = False
        elif key == arcade.key.RIGHT or key == arcade.key.D:
            self.right_pressed = False

        self.process_keychange()

    def on_update(self, delta_time):
        """ Movement and game logic """
        
        
        # moves the boss
        # boss does not move until the player has gotten the potion
        if self.has_potion:
            # calculates the difference between the player's and boss's coordinates 
            difference_x = self.boss_sprite.center_x - self.player_sprite.center_x
            difference_y = self.boss_sprite.center_y - self.player_sprite.center_y
            # the boss will not move if we are too high above him
            if difference_y >= -100:
                # pythagorean theorem to calculate direct distance froom player to boss
                distance = math.sqrt((difference_x ** 2) + (difference_y ** 2))
                # boss only moves if we are close to him
                if distance < 400:
                    self.boss_sprite.change_x = BOSS_MOVEMENT_SPEED
                # there is a spot that the boss can get stuck easily, this fixes that
                elif self.boss_sprite.center_x < 2400 and self.boss_sprite.center_x > 2100:
                    self.boss_sprite.change_x = BOSS_MOVEMENT_SPEED
        # if not all of the requirements are met, the boss stays still    
        else:
            self.boss_sprite.change_x = 0
        
        
        # back and forth movement of the enemies
        if self.enemy_sprite_2.center_x == 700:
            self.enemy_sprite_2.change_x = -ENEMY_MOVEMENT_SPEED
        elif self.enemy_sprite_2.center_x == 520:
            self.enemy_sprite_2.change_x = ENEMY_MOVEMENT_SPEED

        if self.enemy_sprite_3.center_x == 1236:
            self.enemy_sprite_3.change_x = -ENEMY_MOVEMENT_SPEED
        elif self.enemy_sprite_3.center_x == 1060:
            self.enemy_sprite_3.change_x = ENEMY_MOVEMENT_SPEED
        
        if self.enemy_sprite_4.center_x == 320:
            self.enemy_sprite_4.change_x = -ENEMY_MOVEMENT_SPEED
        elif self.enemy_sprite_4.center_x == 160:
            self.enemy_sprite_4.change_x = ENEMY_MOVEMENT_SPEED      
        
        
        # update the physics engines
        self.physics_engine.update()
        self.boss_physics_engine.update()
        self.enemy2_physics_engine.update()
        self.enemy3_physics_engine.update()
        self.enemy4_physics_engine.update()

        
        # Update animations
        if self.physics_engine.can_jump():
            self.player_sprite.can_jump = False
        else:
            self.player_sprite.can_jump = True

        self.player_list.update_animation(delta_time)
        self.enemy_list.update_animation(delta_time)

        
        # check for any collisions
        danger_hit_list = arcade.check_for_collision_with_list(self.player_sprite,
                                                               self.danger_list)
        enemy_hit_list = arcade.check_for_collision_with_list(self.player_sprite,
                                                              self.enemy_list)
        potion_hit_list = arcade.check_for_collision_with_list(self.player_sprite,
                                                      self.potion_list)
        # lose a life if you hit an enemy
        for enemy in enemy_hit_list:
            self.lives = self.lives - 1
            arcade.play_sound(self.jump_sound)
            enemy.remove_from_sprite_lists()
        
        # if there is a potion collision then has potion will be set to true
        for potion in  potion_hit_list:
            potion.remove_from_sprite_lists()
            self.has_potion = True
            

        # Track if we need to change the viewport
        changed_viewport = False

        # --- Manage Scrolling ---

        # Scroll left
        left_boundary = self.view_left + LEFT_VIEWPORT_MARGIN
        if self.player_sprite.left < left_boundary:
            self.view_left -= left_boundary - self.player_sprite.left
            changed_viewport = True

        # Scroll right
        right_boundary = self.view_left + SCREEN_WIDTH - RIGHT_VIEWPORT_MARGIN
        if self.player_sprite.right > right_boundary:
            self.view_left += self.player_sprite.right - right_boundary
            changed_viewport = True

        # Scroll up
        top_boundary = self.view_bottom + SCREEN_HEIGHT - TOP_VIEWPORT_MARGIN
        if self.player_sprite.top > top_boundary:
            self.view_bottom += self.player_sprite.top - top_boundary
            changed_viewport = True

        # Scroll down
        bottom_boundary = self.view_bottom + BOTTOM_VIEWPORT_MARGIN
        if self.player_sprite.bottom < bottom_boundary:
            self.view_bottom -= bottom_boundary - self.player_sprite.bottom
            changed_viewport = True

        if changed_viewport:
            # Only scroll to integers. Otherwise we end up with pixels that
            # don't line up on the screen
            self.view_bottom = int(self.view_bottom)
            self.view_left = int(self.view_left)

            # Do the scrolling
            arcade.set_viewport(self.view_left,
                                SCREEN_WIDTH + self.view_left,
                                self.view_bottom,
                                SCREEN_HEIGHT + self.view_bottom)
