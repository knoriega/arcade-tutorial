# Basic arcade program

import arcade

SCREEN_WIDTH = 600
SCREEN_HEIGHT = 800
SCREEN_TITLE = 'Welcome to Arcade'
RADIUS = 150

# Open window
arcade.open_window(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)

# Bkg Color
arcade.set_background_color(arcade.color.WHITE)

# Clear the screen and start drawing
arcade.start_render()
arcade.draw_circle_filled(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2, RADIUS, arcade.color.BLUE)

# Finish drawing
arcade.finish_render()

# Display everything
arcade.run()
