import arcade
import random
import sys
import functional_Classes
import time

# Set up the constants that set up game window and physics
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN_TITLE = "Pokemon Tester"
VIEWPORT_MARGIN_TOP = 290
VIEWPORT_MARGIN_BOTTOM = 290
VIEWPORT_RIGHT_MARGIN = 390
VIEWPORT_LEFT_MARGIN = 390
movement_speed = 1
width = 16
height = 16


# todo change the walking sprites to animations somehow, a plethora of other stuff
class Player(arcade.Sprite):

    def __init__(self):
        super().__init__()
        # Loads the spritesheet for the character
        textures = arcade.load_spritesheet('Pokemon_project_sprites/trainer_sprites.png', 15, 19, 3, 12)
        self.textures = textures
        self.set_texture(0)

    # call to update player position and sprite
    def update(self):
        """code used to move the player in a grid based way, needs updating to make smoother and slowing down"""
        """if self.change_x > 0:
            self.left = self.right
        elif self.change_x < 0:
            self.right = self.left
        if self.change_y > 0:
            self.bottom = self.top
        elif self.change_y < 0:
            self.top = self.bottom
        self.center_y = self.center_y + self.change_y"""
        self.center_x += self.change_x
        self.center_y += self.change_y

        # describes changes to player sprite based on movement
        # moving left / textures:  6 idle, 7 walk, 8 walk
        if self.change_x < 0:
            self.set_texture(7)
        # moving right / textures: 3 idle, 4 walk, 5 walk
        if self.change_x > 0:
            self.set_texture(4)
        # moving up / textures: 9 idle, 10 walk, 11 walk
        if self.change_y > 0:
            self.set_texture(10)
        # moving down / textures: 0 idle, 1 walk, 2 walk
        if self.change_y < 0:
            self.set_texture(1)
        # temporary return to idle texture function
        if self.change_x == 0 and self.change_y == 0:
            self.set_texture(0)
        # keeps the player on screen assuming they can get past the viewport
        if self.left < 0:
            self.left = 0
        elif self.right > SCREEN_WIDTH - 1:
            self.right = SCREEN_WIDTH - 1
        if self.bottom < 0:
            self.bottom = 0
        elif self.top > SCREEN_HEIGHT - 1:
            self.top = SCREEN_HEIGHT - 1


class MyGame(arcade.Window):
    # set up the game window and any definition needed for class methods
    def __init__(self, w_width, w_height, title):
        super().__init__(w_width, w_height, title)
        self.object_list = None
        self.player_list = None
        self.map = None
        self.player_sprite = None
        self.board = None
        self.left_pressed = False
        self.right_pressed = False
        self.up_pressed = False
        self.down_pressed = False
        self.frame_count = 0
        self.fps_message = None
        self.wall_list = None
        self.room = None
        self.physics_engine = None
        self.view_left = 0
        self.view_right = 0
        self.view_top = 0
        self.view_bottom = 0
        self.last_time = None
        self.background = None

    # initial setup for the game window, puts the player on screen and loads the first map
    # todo, change to load a startup sequence
    def setup(self):
        self.player_list = arcade.SpriteList()
        self.player_sprite = Player()
        self.player_sprite.center_x = 248
        self.player_sprite.center_y = 215
        self.player_list.append(self.player_sprite)
        self.load_level("pallet town")

    # loads the current area, todo, add object interactivity, and add function calls to objects like doors
    def load_level(self, map):
        my_map = arcade.tilemap.read_tmx("New folder/{map}.tmx".format(map=map))
        self.background = arcade.tilemap.process_layer(my_map, 'background')
        self.wall_list = arcade.tilemap.process_layer(my_map, 'walls')
        self.object_list = arcade.tilemap.process_layer(my_map, 'objects')
        self.physics_engine = arcade.PhysicsEngineSimple(self.player_sprite, self.wall_list)
        self.view_left = 0
        self.view_bottom = 0
        self.view_top = 0
        self.view_right = 0

    # draws the area
    def on_draw(self):
        # variable used to setup FPS counter
        self.frame_count += 1
        # starts the rendering process
        arcade.start_render()
        # draws the background of the current map
        self.background.draw()
        # draws the characters sprite
        self.player_list.draw()
        # code to determine sprites location on the current map, for debugging
        self.player_sprite.coordinates = "X: " + str(self.player_sprite.center_x) \
                                         + "\nY: " + str(self.player_sprite.center_y)
        arcade.draw_text(self.player_sprite.coordinates, self.view_left + 10, self.view_bottom + 80,
                         arcade.color.ASH_GREY, 14)
        # code to render the FPS counter, to be removed, or added as an option, doubtful that the framerate
        # will ever become low enough for that to matter
        if self.last_time and self.frame_count % 60 == 0:
            fps = 1.0/(time.time()-self.last_time) * 60
            self.fps_message = f'FPS: {fps:5.0f}'

        if self.fps_message:
            arcade.draw_text(self.fps_message, self.view_left + 10, self.view_bottom + 40, arcade.color.ASH_GREY, 14)

        if self.frame_count % 60 == 0:
            self.last_time = time.time()

    # function used to update the game window, currently only functional for moving the player, will probably use
    # later to add animations
    def on_update(self, delta_time):
        # player movement code, might be depreciated later
        self.player_sprite.change_x = 0
        self.player_sprite.change_y = 0

        if self.up_pressed and not self.down_pressed:
            self.player_sprite.change_y = movement_speed
        elif self.down_pressed and not self.up_pressed:
            self.player_sprite.change_y = -movement_speed
        elif self.left_pressed and not self.right_pressed:
            self.player_sprite.change_x = -movement_speed
        elif self.right_pressed and not self.left_pressed:
            self.player_sprite.change_x = movement_speed
        self.player_sprite.update()
        self.physics_engine.update()
        # code used to keep the player on the center of the screen and move the map around them
        # Scroll left
        changed = False
        left_bndry = self.view_left + VIEWPORT_LEFT_MARGIN
        if self.player_sprite.left < left_bndry:
            self.view_left -= left_bndry - self.player_sprite.left
            changed = True
        # Scroll right
        right_bndry = self.view_left + SCREEN_WIDTH - VIEWPORT_RIGHT_MARGIN
        if self.player_sprite.right > right_bndry:
            self.view_left += self.player_sprite.right - right_bndry
            changed = True
        # Scroll up
        top_bndry = self.view_bottom + SCREEN_HEIGHT - VIEWPORT_MARGIN_TOP
        if self.player_sprite.top > top_bndry:
            self.view_bottom += self.player_sprite.top - top_bndry
            changed = True
        # Scroll down
        bottom_bndry = self.view_bottom + VIEWPORT_MARGIN_BOTTOM
        if self.player_sprite.bottom < bottom_bndry:
            self.view_bottom -= bottom_bndry - self.player_sprite.bottom
            changed = True
        # If we need to scroll, go ahead and do it.
        if changed:
            self.view_left = int(self.view_left)
            self.view_bottom = int(self.view_bottom)
            arcade.set_viewport(self.view_left,
                                SCREEN_WIDTH + self.view_left,
                                self.view_bottom,
                                SCREEN_HEIGHT + self.view_bottom)

    # checks to see which buttons are being pressed, currently only used for player movement
    def on_key_press(self, key, modifiers):
        if key == arcade.key.UP:
            self.up_pressed = True
        elif key == arcade.key.DOWN:
            self.down_pressed = True
        elif key == arcade.key.LEFT:
            self.left_pressed = True
        elif key == arcade.key.RIGHT:
            self.right_pressed = True

    # checks to see when a key is released
    def on_key_release(self, key, modifiers):
        if key == arcade.key.UP:
            self.up_pressed = False
        elif key == arcade.key.DOWN:
            self.down_pressed = False
        elif key == arcade.key.LEFT:
            self.left_pressed = False
        elif key == arcade.key.RIGHT:
            self.right_pressed = False

# starts up the game window
def main():
    window = MyGame(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    window.setup()
    arcade.run()


if __name__ == "__main__":
    main()
