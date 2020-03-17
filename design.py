import arcade
import os

SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 700

SCREEN_TITLE = "MY BEAUTIFUL GAME"

class Game(arcade.Window):

    def __init__(self, width, height, title):
        super().__init__(width, height, title)
        self.shapes_list = arcade.ShapeElementList()

        # Background Gradient
        lower_colour = (255, 193, 204) # BUBBLE_GUM arcade.color package
        upper_colour = (219, 166, 123)
        points = (0, 0), (SCREEN_WIDTH, 0), (SCREEN_WIDTH, SCREEN_HEIGHT), (0, SCREEN_HEIGHT)
        colors = (lower_colour, lower_colour, upper_colour, upper_colour)
        background = arcade.create_rectangle_filled_with_colors(points, colors)
        self.shapes_list.append(background)


        # Creating moon

        circle = arcade.create_ellipse_filled(600,500,60,60,arcade.color.YELLOW_ROSE,0)
        self.shapes_list.append(circle)

        # Creating buildings
        for x in range(0,1200):

            if x % 40 == 0 and x % 80 != 0 :
                colour1 = (86, 60, 92)
                colour2 = (216, 145, 239)
                points = (x, 0), (x+40, 0), (x+40, 100), (x, 100)
                colours = (colour1, colour1, colour2, colour2)
                rect = arcade.create_rectangle_filled_with_colors(points, colours)
                self.shapes_list.append(rect)

            elif x % 80 == 0 and x % 50 != 0:
                colour1 = (255, 248, 231)
                colour2 = (21, 96, 189)
                points = (x, 0), (x+20, 0), (x+20, 200), (x, 200)
                colours = (colour1, colour1, colour2, colour2)
                rect = arcade.create_rectangle_filled_with_colors(points, colours)
                self.shapes_list.append(rect)

            elif x % 60 == 0 and x % 120 != 0:
                colour1 = (27, 27, 27)
                colour2 = (27, 77, 62)
                points = (x, 0), (x+40, 0), (x+40, 300), (x, 300)
                colours = (colour1, colour1, colour2, colour2)
                rect = arcade.create_rectangle_filled_with_colors(points, colours)
                self.shapes_list.append(rect)

            

    def snow(self):
        pass


    def on_draw(self):
        arcade.start_render()  
        for shape in self.shapes_list:
            shape.draw()


def main():

    Game(SCREEN_WIDTH, SCREEN_HEIGHT,SCREEN_TITLE)
    arcade.run()

if __name__ == "__main__":
    main()
