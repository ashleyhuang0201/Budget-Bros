import arcade
import os

SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 700

GRAVITY = 1

SCREEN_TITLE = "MY BEAUTIFUL GAME"
PLAYER_MOVEMENT_SPEED = 5

# scrolling from https://arcade.academy/examples/sprite_move_scrolling.html
LEFT_VIEWPORT_MARGIN = 150
RIGHT_VIEWPORT_MARGIN = 150
BOTTOM_VIEWPORT_MARGIN = 50
TOP_VIEWPORT_MARGIN = 100

class Game(arcade.Window):

    def __init__(self):
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
        self.score = 0
        self.timer = 0.0
        self.physics_engine = None
        self.blocks = None
        self.players= None
        # self.enemies = None

        self.player_sprite = None
        self.physics_engine = None
        self.game_over = False

        # Background Gradient

        self.shapes_list = arcade.ShapeElementList()
        lower_colour = (255, 193, 204) # BUBBLE_GUM arcade.color package
        upper_colour = (219, 166, 123)
        points = (0, 0), (SCREEN_WIDTH, 0), (SCREEN_WIDTH, SCREEN_HEIGHT), (0, SCREEN_HEIGHT)
        colors = (lower_colour, lower_colour, upper_colour, upper_colour)
        background = arcade.create_rectangle_filled_with_colors(points, colors)
        self.shapes_list.append(background)

        # Creating moon

        circle = arcade.create_ellipse_filled(600,500,60,60,arcade.color.WHITE_SMOKE,0)
        self.shapes_list.append(circle)
        
        '''
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

        '''
        # MOVING SCREEN TRACKING
        self.view_bottom = 0
        self.view_left = 0

    # when game restarts
    def setup(self):
        self.timer = 0.0

        # set up scrolling
        self.view_bottom = 0
        self.view_left = 0

        # set up lists for players and walls
        self.players = arcade.SpriteList()
        self.blocks = arcade.SpriteList()

        # set up player 
        self.player_sprite = arcade.Sprite("player1_image/female_back.png", 0.5)

        # set up starting position for player
        self.player_sprite.center_x = 100
        self.player_sprite.center_y = 400

        # set up enemies
        self.enemies = arcade.SpriteList()

        starting_position = 128
        for i in range(0,5):
            enemy = arcade.Sprite("player1_image/my_player.png", 0.1)
            enemy.bottom = 128
            enemy.left = starting_position
            enemy.boundary_right = 1800
            enemy.boundary_left = 0
            # enemies speed, change this for harder difficulty
            enemy.change_x = 4
            self.enemies.append(enemy)
            starting_position += 400


        # add player_sprite to the list
        self.players.append(self.player_sprite)

        # loading in map
        map_name = "player_map/new.tmx"
        
        # Name of the layer in the file that has our platforms/walls
        platform_layer = 'Platforms'
        background_layer = 'Background'

        # Read in the tiled map
        my_map = arcade.read_tiled_map(map_name, 1)
        map_array = my_map.layers_int_data[platform_layer]

        # walls and background to draw out later
        # change variables later

        self.blocks = arcade.generate_sprites(my_map, platform_layer, 1)
        self.background_list = arcade.generate_sprites(my_map, background_layer, 1)

        self.physics_engine = arcade.PhysicsEnginePlatformer(self.player_sprite, self.blocks, GRAVITY)


    def snow(self):
        pass

    

    def on_draw(self):
        arcade.start_render()  
        for shape in self.shapes_list:
            shape.draw()

        # calculate minutes
        minutes = int(self.timer) // 60

        # calculate seconds 
        seconds = int(self.timer) % 60

        output = f"Time: {minutes:02d}:{seconds:02d}"

        # player_sprite's score that is generated by time survived
        arcade.draw_text(output, 1000, 650, arcade.color.WHITE, 30)

    
        # draw background first - base layer
        self.background_list.draw()
        
        # draw walls next 
        self.blocks.draw()
       
       # draw the player on top
        self.players.draw()
        
        # draw enemies
        self.enemies.draw()

    def on_key_press(self, key, modifiers):
        if key == arcade.key.UP:
            if self.physics_engine.can_jump():
                self.player_sprite.change_y = 15 # jump speed
        elif key == arcade.key.LEFT:
            self.player_sprite.change_x = -PLAYER_MOVEMENT_SPEED
        elif key == arcade.key.RIGHT:
            self.player_sprite.change_x = PLAYER_MOVEMENT_SPEED

    def on_key_release(self, key, modifiers):
        if key == arcade.key.LEFT:
            self.player_sprite.change_x = 0
        elif key == arcade.key.RIGHT:
            self.player_sprite.change_x = 0
    

    def on_update(self, delta_time):
        self.timer += delta_time

        # from https://arcade.academy/examples/sprite_move_scrolling.html
        changed = False

        # Scroll left
        left_boundary = self.view_left + LEFT_VIEWPORT_MARGIN
        if self.player_sprite.left < left_boundary:
            self.view_left -= left_boundary - self.player_sprite.left
            changed = True

        # Scroll right
        right_boundary = self.view_left + SCREEN_WIDTH - RIGHT_VIEWPORT_MARGIN
        if self.player_sprite.right > right_boundary:
            self.view_left += self.player_sprite.right - right_boundary
            changed = True

        # Scroll up
        top_boundary = self.view_bottom + SCREEN_HEIGHT - TOP_VIEWPORT_MARGIN
        if self.player_sprite.top > top_boundary:
            self.view_bottom += self.player_sprite.top - top_boundary
            changed = True

        # Scroll down
        bottom_boundary = self.view_bottom + BOTTOM_VIEWPORT_MARGIN
        if self.player_sprite.bottom < bottom_boundary:
            self.view_bottom -= bottom_boundary - self.player_sprite.bottom
            changed = True

        if changed:
            # Only scroll to integers. Otherwise we end up with pixels that
            # don't line up on the screen
            self.view_bottom = int(self.view_bottom)
            self.view_left = int(self.view_left)

            # Do the scrolling
            arcade.set_viewport(self.view_left,
                                SCREEN_WIDTH + self.view_left,
                                self.view_bottom,
                                SCREEN_HEIGHT + self.view_bottom)

        # Did the player fall off the map?
        if self.player_sprite.center_y < -100:
            self.player_sprite.center_x = 100
            self.player_sprite.center_y = 100

            # Set the camera to the start
            self.view_left = 0
            self.view_bottom = 0
            changed_viewport = True
            self.game_over = True

        if not self.game_over:
            self.enemies.update()
            # for every enemy, check if they hit anything
            for enemy in self.enemies:
                # If the enemy hit a wall, change direction
                if len(arcade.check_for_collision_with_list(enemy, self.blocks)) > 0:
                    enemy.change_x *= -1



        if len(arcade.check_for_collision_with_list(self.player_sprite, self.enemies)) > 0:
            self.game_over = True
            self.player_sprite.center_x = 400
            self.player_sprite.center_y = 400

            # Set the camera to the start
            self.view_left = 0
            self.view_bottom = 0
            changed_viewport = True

        if self.game_over == True:
            pass  

        self.physics_engine.update()
            
def main():

    window = Game()
    window.setup()
    arcade.run()

if __name__ == "__main__":
    main()
