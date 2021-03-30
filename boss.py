import arcade


def load_texture_pair(filename):
    """
    Load a texture pair, with the second being a mirror image.
    """
    return [
        arcade.load_texture(filename),
        arcade.load_texture(filename, flipped_horizontally=True)
    ]


class BossCharacter(arcade.Sprite):
    """enemy sprite animations"""
    def __init__(self):
        
        # set up parent class
        super().__init__()

        # used for flipping between image sequences
        self.scale = BOSS_SCALING
        self.cur_texture = 0

        # load idle textures
        self.idle_texture_pair = load_texture_pair("artwork/angry_king/angry_king_idle.png")

        # load walking textures
        self.walk_textures = []
        for i in range(1,11):
            texture = load_texture_pair(f"artwork/angry_king/angry_king_walk{i}.png")
            self.walk_textures.append(texture)

        # set initial texture
        self.texture = self.idle_texture_pair[1]

    def update_animation(self, delta_time: float = 1/60):

        # walking animation
        self.cur_texture += 1
        if self.cur_texture > 9:
            self.cur_texture = 0
        self.texture = self.walk_textures[self.cur_texture][1]

        # check if boss is idle
        if self.change_x == 0:
            self.texture = self.idle_texture_pair[1]
