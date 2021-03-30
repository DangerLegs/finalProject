import arcade

RIGHT_FACING = 0
LEFT_FACING = 1

def load_texture_pair(filename):
    """
    Load a texture pair, with the second being a mirror image.
    """
    return [
        arcade.load_texture(filename),
        arcade.load_texture(filename, flipped_horizontally=True)
    ]

  class EnemyCharacter(arcade.Sprite):
    """enemy sprite animations"""
    def __init__(self):
        
        # set up parent class
        super().__init__()
        
        # used for determining the direction of the enemy
        self.character_face_direction = RIGHT_FACING

        # used for flipping between image sequences
        self.scale = ENEMY_SCALING
        self.cur_texture = 7

        # load walking textures
        self.walk_textures = []
        for i in range(1,8):
            texture = load_texture_pair(f"artwork/stego/stego_walk{i}.png")
            self.walk_textures.append(texture)

        # set initial texture
        self.texture = self.walk_textures[6][self.character_face_direction]

    def update_animation(self, delta_time: float = 1/60):

        # Figure out if we need to flip face left or right
        if self.change_x < 0 and self.character_face_direction == RIGHT_FACING:
            self.character_face_direction = LEFT_FACING
        elif self.change_x > 0 and self.character_face_direction == LEFT_FACING:
            self.character_face_direction = RIGHT_FACING

        # walking animation
        self.cur_texture -= 1
        if self.cur_texture < 0:
            self.cur_texture = 6
        self.texture = self.walk_textures[self.cur_texture][self.character_face_direction]
