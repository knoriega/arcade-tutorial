# Basic arcade shooter

import arcade
import random

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN_TITLE = 'Arcade Space Shooter'
SCALING = 1.0


class FlyingSprite(arcade, Sprite):
    """Base class for all flying sprites
    Flying sprites include enemies and clouds
    """

    def update(self):
        """Update the position of the sprite
        When it moves off-screen to the left, remove it
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

    def on_draw(self):
        """Called whenever you need to draw on your window"""
        arcade.start_render()

        # Draw everything we know about?
        self.all_sprites.draw()

    def add_enemy(self, delta_time: float):
        """Adds a new enemy to the screen

        Args:
            delta_time {float} -- How much time has passed since last call (required by arcade.schedule)
        """

        # 1. Create new enemy sprite
        enemy = arcade.FlyingSprite('images/missile.png', SCALING)

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
