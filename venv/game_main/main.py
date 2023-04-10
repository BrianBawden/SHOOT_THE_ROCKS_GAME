"""
This is my shooting game I made using arcade with python. I used VS Code as my IDE.

References:
* https://api.arcade.academy/en/latest/index.html
* https://www.youtube.com/playlist?list=PL1P11yPQAo7pPlDlFEaL3IUbcWnnPcALI

"""

import arcade
import random

# Global variables to use in the program. 
SPRITE_SCALE_PLAYER = 0.75
SPRITE_SCALE_METEOR = 0.75
SPRITE_SCALE_LASER = 0.8

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN_TITLE = "SHOOT THE BIG ROCKS!!!"

LASER_SPEED = 10
METEOR_SPEED = 2
SPRITE_START_X = 50
SPRITE_START_Y = 70

# Class for the shoot the big rocks
class MyGame(arcade.Window):
    # Constructor of game 
    def __init__(self):
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE,)

        arcade.set_background_color(arcade.color.BLACK)

        self.player_list = None
        self.meteor_list = None
        self.laser_list = None

        self.player_sprite = None
        self.score = 0
        self.score_text = None

        self.laser_sound = arcade.sound.load_sound(":resources:sounds/laser1.wav")
        self.hit_sound = arcade.sound.load_sound(":resources:sounds/phaseJump1.wav")
        self.your_dead_sound = arcade.sound.load_sound(":resources:sounds/error1.wav")


    def setup(self):
        # Using the arcade library to construct the different sprites like ship, meteors, and laser.
        global METEOR_SPEED
        self.player_list = arcade.SpriteList()
        self.laser_list = arcade.SpriteList()
        self.meteor_list = arcade.SpriteList()

        self.score = 0

        self.player_sprite = arcade.Sprite(":resources:images/space_shooter/"
        "playerShip1_blue.png", SPRITE_SCALE_PLAYER)
        self.player_sprite.center_x = SPRITE_START_X
        self.player_sprite.center_y = SPRITE_START_Y
        self.player_list.append(self.player_sprite)

        arcade.set_background_color(arcade.color.BLACK)

        for _ in range(10):
            self.create_meteor()
            

    def create_meteor(self):
            meteor = arcade.Sprite(":resources:images/space_shooter/meteorGrey_med1.png", SPRITE_SCALE_METEOR)
            meteor.center_x = random.randrange(20, SCREEN_WIDTH - 25) 
            meteor.center_y = random.randrange(SCREEN_HEIGHT + 10, SCREEN_HEIGHT + 1110)

            meteor.change_y -= METEOR_SPEED
            self.meteor_list.append(meteor)

    def on_draw(self):
        
        self.clear()

        self.player_list.draw()
        self.laser_list.draw()
        self.meteor_list.draw()

        score_output = f"Score: {self.score}"
        arcade.draw_text(score_output, 10, 20, arcade.color.WHITE, 14)

    def on_update(self, delta_time: float):
        global METEOR_SPEED
        self.laser_list.update()
        self.meteor_list.update()

        if arcade.check_for_collision_with_list(self.player_sprite, self.meteor_list):
            arcade.play_sound(self.your_dead_sound)
            self.setup()

        for l in self.laser_list: 
            hit_list = arcade.check_for_collision_with_list(l, self.meteor_list)

            if len(hit_list) > 0:
                l.remove_from_sprite_lists()
                arcade.play_sound(self.hit_sound)


            for m in hit_list:
                m.remove_from_sprite_lists()
                self.score += 1
                self.create_meteor()


                if self.score % 10 == 0:
                    color_r = random.randrange(0, 250)
                    color_g = random.randrange(0, 250)
                    color_b = random.randrange(0, 250)
                    arcade.set_background_color((color_r, color_g, color_b))
                    METEOR_SPEED += 2
            if l.top > SCREEN_HEIGHT:
                l.remove_from_sprite_lists()

        for m in self.meteor_list:
            if m.bottom < 0:
                m.remove_from_sprite_lists()
                self.create_meteor()


    def on_mouse_motion(self, x: int, y: int, dx: int, dy: int):
        self.player_sprite.center_x = x
        self.player_sprite.center_y = y
        

    def on_mouse_press(self, x: int, y: int, button: int, modifiers: int):
        laser = arcade.Sprite(":resources:images/space_shooter/laserBlue01.png", SPRITE_SCALE_LASER)
        arcade.play_sound(self.laser_sound)

        laser.turn_left(90)

        laser.center_x = x 
        laser.center_y = y 
        laser.change_y += LASER_SPEED

        self.laser_list.append(laser)

    def create_meteor(self):
        meteor = arcade.Sprite(":resources:images/space_shooter/meteorGrey_med1.png", SPRITE_SCALE_METEOR)
        meteor.center_x = random.randrange(20, SCREEN_WIDTH - 25) 
        meteor.center_y = random.randrange(SCREEN_HEIGHT + 10, SCREEN_HEIGHT + 1110)

        meteor.change_y -= METEOR_SPEED
        self.meteor_list.append(meteor)



def main():
        game = MyGame()
        game.setup()
        arcade.run()

if __name__ == "__main__":
    main()