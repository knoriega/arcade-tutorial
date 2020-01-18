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

        # Start game not paused
        self.paused = False

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

        # If paused don't do anything
        if self.paused:
            return

        # Did player hit anything? If so, end the game!
        #   Subtlety: check for collision before drawing anything
        if self.player.collides_with_list(self.enemies_list):
            arcade.close_window()

        # Update everything to show movement!
        self.all_sprites.update()

        # Keep player on screen
        if self.player.top > self.height:
            self.player.top = self.height
        if self.player.right > self.width:
            self.player.right = self.width
        if self.player.bottom < 0:
            self.player.bottom = 0
        if self.player.left < 0:
            self.player.left = 0

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
            self.player.change_y = 5

        if symbol == arcade.key.J or symbol == arcade.key.LEFT:
            self.player.change_x = -5

        if symbol == arcade.key.K or symbol == arcade.key.DOWN:
            self.player.change_y = -5

        if symbol == arcade.key.L or symbol == arcade.key.RIGHT:
            self.player.change_x = 5

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

        # 1. Create new enemy sprite
        enemy = FlyingSprite('images/missile.png', SCALING)

        # 2. Set position to a random height and off screen right
        enemy.left = random.randint(self.width, self.width + 80)
        enemy.top = random.randint(10, self.height - 10)

        # 3. Set movement speed -- motion attributes can handle movements during update() calls
        enemy.velocity = (random.randint(-20, -5), 0)

        # 4. Add it to the enemies and all_sprites list
        self.enemies_list.append(enemy)
        self.all_sprites.append(enemy)

    def add_cloud(self, delta_time: float):
        """Adds a new cloud to the screen

        Args:
            delta_time {float} -- How much time has passed since last call (required by arcade.schedule)
        """
        # 1. Create cloud
        cloud = FlyingSprite('images/cloud.png')

        # 2. Set its positions to a random height and off screen right
        cloud.left = random.randint(self.width, self.width + 80)
        cloud.top = random.randint(10, self.height - 10)

        # 3. Set speed to a random slow speed heading left
        cloud.velocity = (random.randint(-5, -2), 0)

        # 4.Add it to the enemies list
        self.clouds_list.append(cloud)
        self.all_sprites.append(cloud)


if __name__ == '__main__':
    app = SpaceShooter(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    app.setup()
    arcade.run()
