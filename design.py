import arcade

def white_circle(x, y):
    arcade.draw_circle_filled(x,y, 40, arcade.color.WHITE, 40)


def main():

    SCREEN_WIDTH = 1600
    SCREEN_HEIGHT = 900
    arcade.open_window(SCREEN_WIDTH, SCREEN_HEIGHT, "Game")

    arcade.set_background_color(arcade.color.BLACK)

    arcade.start_render()
    white_circle(500,500)

    arcade.finish_render()

    arcade.run()

if __name__ == "__main__":
    main()
