# Basic arcade shooter

import arcade
import random

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN_TITLE = 'Arcade Space Shooter'
SCALING = 1.0


class FlyingSprite(arcade.Sprite):
    """Base class for all flying sprites
    Flying sprites include enemies and clouds
    """

    def update(self):
        """Update the position of the sprite
        When it moves off-screen to the left, remove it!
        """

        # Move the sprite
        super().update()

        # Remove if off screen
        if self.right < 0:
            self.remove_from_sprite_lists()


class SpaceShooter(arcade.Window):
    """Space Shooter side scroller
    Player starts on the left, enemies appear on the right
    Player can move anywhere, but not off screen
    Enemies fly to the left at variable speed
    Collisions end the game
    """

    def __init__(self, width, height, title):
        """Initialize the game"""
        super().__init__(width, height, title)

        # Set up the empty sprite lists
        # SpriteList has a lot of convenient methods
        #   .draw() for drawing all sprites in list
        #   .update() updating states
        #   can check if any sprite has collided with any sprite in the list
        self.enemies_list = arcade.SpriteList()
        self.clouds_list = arcade.SpriteList()
        self.all_sprites = arcade.SpriteList()

    def setup(self):
        """Get the game ready to play"""

        # Set bkg color
        arcade.set_background_color(arcade.color.SKY_BLUE)

        # Set up the player
        self.player = arcade.Sprite('images/jet.png', SCALING)
        self.player.center_y = self.height / 2
        self.player.left = 10
        self.all_sprites.append(self.player)

        # Spawn new enemy every 0.25 seconds -- define self.add_enemy!
        arcade.schedule(self.add_enemy, 0.25)

        # Spawn new cloud every second -- define self.add_cloud!
        arcade.schedule(self.add_cloud, 1.0)

        # Load bkg music
        # Sound source: http://ccmixter.org/files/Apoxode/59262
        # License: https://creativecommons.org/licenses/by/3.0/
        self.background_music = arcade.load_sound(
            "sounds/Apoxode_-_Electric_1.wav"
        )

        # Load in sounds
        # Sounds sources: Jon Fincher
        self.collision_sound = arcade.load_sound('sounds/Collision.wav')
        self.move_up_sound = arcade.load_sound('sounds/Rising_putter.wav')
        self.move_down_sound = arcade.load_sound('sounds/Falling_putter.wav')

        # Start the background music
        arcade.play_sound(self.background_music)

        # Start game unpaused
        self.paused = False

        # Collision timer to play sound
        self.collided = False
        self.collision_timer = 0.0

        # Bkg music timer to loop music
        self.bkg_music_timer = 0.0

    def on_draw(self):
        """Draw all game objects"""
        arcade.start_render()
        self.all_sprites.draw()

    def on_update(self, delta_time: float):
        """Updates the positions and statuses of all game objects
        If paused, do nothing

        Args:
            delta_time {float} -- Time since last update
        """

        # Did we collided with anything earlier? If so, update timer
        if self.collided:
            self.collision_timer += delta_time

            # If the window has stayed open for 1 second, close it
            if self.collision_timer > 1.0:
                arcade.close_window()

            # Stop updating once we've collided
            return

        # If paused don't do anything
        if self.paused:
            return

        # Did player hit anything? If so, end the game!
        #   Subtlety: check for collision before drawing anything
        if len(self.player.collides_with_list(self.enemies_list)) > 0:
            self.collided = True
            self.collision_timer = 0.0
            arcade.play_sound(self.collision_sound)

        # Update positions manually to account for framerate
        for sprite in self.all_sprites:
            sprite.center_x = int(
                sprite.center_x + sprite.change_x * delta_time
            )

            sprite.center_y = int(
                sprite.center_y + sprite.change_y * delta_time
            )

        # Keep player on screen
        if self.player.top > self.height:
            self.player.top = self.height
        if self.player.right > self.width:
            self.player.right = self.width
        if self.player.bottom < 0:
            self.player.bottom = 0
        if self.player.left < 0:
            self.player.left = 0

        # Increment bkg music timer and loop it if we need to
        self.bkg_music_timer += delta_time

        if self.bkg_music_timer > 15:
            self.bkg_music_timer = 0.0
            arcade.play_sound(self.background_music)

    def on_key_press(self, symbol, modifiers):
        """Handle user keyboard input
        Q: Quit the game
        P: Pause/Unpause
        I/J/K/L: Move up, left, down, right
        Arrows: Move up, left, down, right

        Args:
            symbol {int} -- Which key was pressed
            modifier {int} -- Which modifiers were pressed
        """

        if symbol == arcade.key.Q:
            # Quit immediately
            arcade.close_window()

        if symbol == arcade.key.P:
            self.paused = not self.paused

        if symbol == arcade.key.I or symbol == arcade.key.UP:
            self.player.change_y = 250
            arcade.play_sound(self.move_up_sound)

        if symbol == arcade.key.J or symbol == arcade.key.LEFT:
            self.player.change_x = -250

        if symbol == arcade.key.K or symbol == arcade.key.DOWN:
            self.player.change_y = -250
            arcade.play_sound(self.move_down_sound)

        if symbol == arcade.key.L or symbol == arcade.key.RIGHT:
            self.player.change_x = 250

    def on_key_release(self, symbol, modifiers):
        """Undo movement vectors when movement keys are released

        Args:
            symbol {int} -- Which key was pressed
            modifiers {int} -- Which modifiers were pressed
        """

        if (
            symbol == arcade.key.I
            or symbol == arcade.key.K
            or symbol == arcade.key.UP
            or symbol == arcade.key.DOWN
        ):
            self.player.change_y = 0

        if (
            symbol == arcade.key.J
            or symbol == arcade.key.L
            or symbol == arcade.key.LEFT
            or symbol == arcade.key.RIGHT
        ):
            self.player.change_x = 0

    def add_enemy(self, delta_time: float):
        """Adds a new enemy to the screen

        Args:
            delta_time {float} -- How much time has passed since last call (required by arcade.schedule)
        """

        # Don't add an enemy if the game is paused
        if self.paused:
            return

        # 1. Create new enemy sprite
        enemy = FlyingSprite('images/missile.png', SCALING)

        # 2. Set position to a random height and off screen right
        enemy.left = random.randint(self.width, self.width + 80)
        enemy.top = random.randint(10, self.height - 10)

        # 3. Set movement speed -- motion attributes can handle movements during update() calls
        enemy.velocity = (random.randint(-200, -50), 0)

        # 4. Add it to the enemies and all_sprites list
        self.enemies_list.append(enemy)
        self.all_sprites.append(enemy)

    def add_cloud(self, delta_time: float):
        """Adds a new cloud to the screen

        Args:
            delta_time {float} -- How much time has passed since last call (required by arcade.schedule)
        """

        # Don't add cloud if the game is paused
        if self.paused:
            return

        # 1. Create cloud
        cloud = FlyingSprite('images/cloud.png')

        # 2. Set its positions to a random height and off screen right
        cloud.left = random.randint(self.width, self.width + 80)
        cloud.top = random.randint(10, self.height - 10)

        # 3. Set speed to a random slow speed heading left
        cloud.velocity = (random.randint(-50, -20), 0)

        # 4.Add it to the enemies list
        self.clouds_list.append(cloud)
        self.all_sprites.append(cloud)


if __name__ == '__main__':
    app = SpaceShooter(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    app.setup()
    arcade.run()
