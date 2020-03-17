import arcade
import os

SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 700

SCREEN_TITLE = "MY BEAUTIFUL GAME"

class Game(arcade.Window):

    def __init__(self, width, height, title):
        super().__init__(width, height, title)
        arcade.set_background_color(arcade.color.BLUE)

        self.shapes = arcade.ShapeElementList()

        lower_colour = (255, 193, 204) # BUBBLE_GUM arcade.color package
        upper_colour = (219, 166, 123)
        points = (0, 0), (SCREEN_WIDTH, 0), (SCREEN_WIDTH, SCREEN_HEIGHT), (0, SCREEN_HEIGHT)
        colors = (lower_colour, lower_colour, upper_colour, upper_colour)
        background = arcade.create_rectangle_filled_with_colors(points, colors)
        self.shapes.append(background)


    def on_draw(self):
        arcade.start_render()
        self.shapes.draw()


def main():

    Game(SCREEN_WIDTH, SCREEN_HEIGHT,SCREEN_TITLE)
    arcade.run()

if __name__ == "__main__":
    main()
