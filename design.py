import arcade
import os
import random
import time

SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 700

GRAVITY = 0.8

SCREEN_TITLE = "MY BEAUTIFUL GAME"
PLAYER_MOVEMENT_SPEED = 5

# scrolling from https://arcade.academy/examples/sprite_move_scrolling.html
LEFT_VIEWPORT_MARGIN = 150
RIGHT_VIEWPORT_MARGIN = 150
BOTTOM_VIEWPORT_MARGIN = 50
TOP_VIEWPORT_MARGIN = 100

WIDTH = 1200
HEIGHT = 700



class MenuView(arcade.View):
    def on_show(self):
        arcade.set_background_color(arcade.color.LIGHT_PINK)

    def on_draw(self):
        arcade.start_render()
        texture = arcade.load_texture("player_map/start_screen.png")
        arcade.draw_scaled_texture_rectangle(WIDTH/2,HEIGHT/2, texture,1,0) 
        

    def on_mouse_press(self, _x, _y, _button, _modifiers):
        game_view = GameView()
        game_view.setup()
        self.window.show_view(game_view)

class GameView(arcade.View):

    def __init__(self):
        super().__init__()
        self.score = 0
        self.total_time = 0.0
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
        
        # MOVING SCREEN TRACKING
        self.view_bottom = 0
        self.view_left = 0

    # when game restarts
    def setup(self):
        self.total_time = 0.0

        # set up scrolling
        self.view_bottom = 0
        self.view_left = 0

        # set up lists for players and walls
        self.players = arcade.SpriteList()
        self.blocks = arcade.SpriteList()

        # set up player 
        self.player_sprite = arcade.Sprite("player1_image/blob.png", 0.05)

        # set up starting position for player
        self.player_sprite.center_x = 100
        self.player_sprite.center_y = 400

        # set up enemies
        self.enemies = arcade.SpriteList()

        starting_position = 80
        for i in range(0,4):
            enemy = arcade.Sprite("player1_image/my_player.png", 0.1)
            enemy.bottom = 128
            enemy.left = starting_position
            enemy.boundary_right = 1800
            enemy.boundary_left = 0
            # enemies speed, change this for harder difficulty
            enemy.change_x = 3
            self.enemies.append(enemy)
            starting_position += 500

        start_lol = 100
        for j in range(0,2):
            enemy =  arcade.Sprite("player1_image/my_player.png", 0.1)
            enemy.bottom = 128
            enemy.left = start_lol
            enemy.boundary_right = 1800
            enemy.boundary_left = 0
            # enemies speed, change this for harder difficulty
            enemy.change_x = 5
            self.enemies.append(enemy)
            start_lol += 500



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

    def on_draw(self):
        arcade.start_render()  
        for shape in self.shapes_list:
            shape.draw()

        # calculate minutes
        minutes = int(self.total_time) // 60

        # calculate seconds 
        seconds = int(self.total_time) % 60

        output = f"Time: {minutes:02d}:{seconds:02d}"

        # player_sprite's score that is generated by time survived
        arcade.draw_text(output, 1000, 650, arcade.color.WHITE, 30, anchor_x="center")

    
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
        self.total_time += delta_time

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
            arcade.set_viewport(self.view_left,SCREEN_WIDTH + self.view_left, self.view_bottom, SCREEN_HEIGHT + self.view_bottom)

        # Did the player fall off the map?
        if self.player_sprite.center_y < -100:
            self.player_sprite.center_x = 100
            self.player_sprite.center_y = 100
            arcade.set_viewport(0,SCREEN_WIDTH, 0, SCREEN_HEIGHT)
            # Set the camera to the start
            self.view_left = 0
            self.view_bottom = 0
            self.game_over = True

        if not self.game_over:
            self.enemies.update()
            # for every enemy, check if they hit anything
            for enemy in self.enemies:
                # If the enemy hit a wall, change direction
                if len(arcade.check_for_collision_with_list(enemy, self.blocks)) > 0:
                    enemy.change_x *= -1

        
        if len(arcade.check_for_collision_with_list(self.player_sprite, self.enemies)) > 0:
            list_of_questions = [GamePauseView(self),GamePauseView2(self),GamePauseView3(self), \
            GamePauseView4(self), GamePauseView5(self), GamePauseView6(self), GamePauseView7(self), \
            GamePauseView8(self)]
         

            pause_screen = random.choice(list_of_questions)
            pause_screen.total_time = self.total_time
            self.window.show_view(pause_screen)
            

            # reset the camera so that when the pause resumes, it does not cause the player to continue colliding with the enemy
            self.player_sprite.center_x = 400
            self.player_sprite.center_y = 400
            self.view_left = 0
            self.view_bottom = 0
            
            arcade.set_viewport(self.view_left,SCREEN_WIDTH, self.view_bottom, SCREEN_HEIGHT)

        self.physics_engine.update()
list_time = []
class GameOverView(arcade.View):
    def __init__(self):
        super().__init__()
        self.total_time = 0

    def on_show(self):
        arcade.set_background_color(arcade.color.GRAY_BLUE)

    def on_draw(self):
        arcade.start_render()
        texture = arcade.load_texture("player_map/game_over.png")
        arcade.draw_scaled_texture_rectangle(WIDTH/2,HEIGHT/2, texture,1,0) 
        
        total_time_taken = f"{round(self.total_time, 2)} seconds"
        arcade.draw_text(f"TIME TAKEN: {total_time_taken}",WIDTH/2, 370, arcade.color.GRAY,font_size=17, anchor_x="center")
       
        # append if the time is not already in the list and if there is less than 10 items
        if round(self.total_time,2) not in list_time and len(list_time) < 10:
            list_time.append(round(self.total_time,2))
        # if there is more than 10 items and the new item is larger than the smallest item,
        # remove the smallest time record and add in the new time record
        elif round(self.total_time,2) not in list_time and len(list_time) >= 10:
            list_time.sort()
            if round(self.total_time,2) > list_time[0]:
                list_time.remove(list_time[0])
                list_time.append(round(self.total_time,2))

    def on_key_press(self, key, _modifiers):
        if key == arcade.key.ESCAPE:
            leaderboard = Leaderboard()
            self.window.show_view(leaderboard)


class Leaderboard(arcade.View):
    def __init__(self):
        super().__init__()
        self.total_time = 0

    def on_show(self):
        arcade.set_background_color(arcade.color.GRAY_BLUE)

    def on_draw(self):
        arcade.start_render()

        # texture of TOP 10 RECORDS
        texture = arcade.load_texture("player_map/leaderboard.png")
        arcade.draw_scaled_texture_rectangle(WIDTH/2,HEIGHT/2, texture,1,0) 


        list_time.sort()
        j = 100
        for i in range(len(list_time)):
            arcade.draw_text(str(list_time[i]),WIDTH/2, j, arcade.color.WHITE,font_size=25, anchor_x="center")
            j += 40

        arcade.draw_text("PRESS ESC TO CONTINUE",WIDTH/2, 510, arcade.color.WHITE,font_size=15, anchor_x="center")

    def on_key_press(self, key, _modifiers):
        if key == arcade.key.ESCAPE:
            menu_view = MenuView()
            self.window.show_view(menu_view)
    

# append all of them to one list and draw them 
class GamePauseView(arcade.View):

    def __init__(self, game_view):
        super().__init__()
        self.total_time = 0
        self.game_view = game_view

    def on_draw(self):
        arcade.start_render()
        texture = arcade.load_texture("questions/sec1.png")
        arcade.draw_scaled_texture_rectangle(WIDTH/2,HEIGHT/2, texture,1,0) 

    def on_key_press(self, key, _modifiers):
        if key != arcade.key.RIGHT and key != arcade.key.LEFT and key != arcade.key.UP and key != arcade.key.DOWN:
            if key != arcade.key.B:
                game_over = GameOverView()
                game_over.total_time = self.total_time
                self.window.show_view(game_over)

            else:
                self.window.show_view(self.game_view)



class GamePauseView2(arcade.View):

    def __init__(self, game_view):
        super().__init__()
        self.game_view = game_view
        self.total_time = 0
    
    def on_draw(self):
        arcade.start_render()
        texture = arcade.load_texture("questions/sec2.png")
        arcade.draw_scaled_texture_rectangle(WIDTH/2,HEIGHT/2, texture,1,0) 

    def on_key_press(self, key, _modifiers):
        if key != arcade.key.RIGHT and key != arcade.key.LEFT and key != arcade.key.UP and key != arcade.key.DOWN:
            if key != arcade.key.C:
                game_over = GameOverView()
                game_over.total_time = self.total_time
                self.window.show_view(game_over)
            else:
                self.window.show_view(self.game_view)

class GamePauseView3(arcade.View):
    def __init__(self, game_view):
        super().__init__()
        self.game_view = game_view
        self.total_time = 0
    
    def on_draw(self):
        arcade.start_render()
        texture = arcade.load_texture("questions/sec3.png")
        arcade.draw_scaled_texture_rectangle(WIDTH/2,HEIGHT/2, texture,1,0) 

    def on_key_press(self, key, _modifiers):
        if key != arcade.key.RIGHT and key != arcade.key.LEFT and key != arcade.key.UP and key != arcade.key.DOWN:
            if key != arcade.key.A:
                game_over = GameOverView()
                game_over.total_time = self.total_time
                self.window.show_view(game_over)
            else:
                self.window.show_view(self.game_view)

class GamePauseView4(arcade.View):
    def __init__(self, game_view):
        super().__init__()
        self.game_view = game_view
        self.total_time = 0
    
    def on_draw(self):
        arcade.start_render()
        texture = arcade.load_texture("questions/sec4.png")
        arcade.draw_scaled_texture_rectangle(WIDTH/2,HEIGHT/2, texture,1,0) 

    def on_key_press(self, key, _modifiers):
        if key != arcade.key.RIGHT and key != arcade.key.LEFT and key != arcade.key.UP and key != arcade.key.DOWN:
            if key != arcade.key.D:
                game_over = GameOverView()
                game_over.total_time = self.total_time
                self.window.show_view(game_over)
            else:
                self.window.show_view(self.game_view)

class GamePauseView5(arcade.View):
    def __init__(self, game_view):
        super().__init__()
        self.game_view = game_view
        self.total_time = 0
    
    def on_draw(self):
        arcade.start_render()
        texture = arcade.load_texture("questions/sec5.png")
        arcade.draw_scaled_texture_rectangle(WIDTH/2,HEIGHT/2, texture,1,0) 

    def on_key_press(self, key, _modifiers):
        if key != arcade.key.RIGHT and key != arcade.key.LEFT and key != arcade.key.UP and key != arcade.key.DOWN:
            if key != arcade.key.A:
                game_over = GameOverView()
                game_over.total_time = self.total_time
                self.window.show_view(game_over)
            else:
                self.window.show_view(self.game_view)

class GamePauseView6(arcade.View):
    def __init__(self, game_view):
        super().__init__()
        self.game_view = game_view
        self.total_time = 0
    
    def on_draw(self):
        arcade.start_render()
        texture = arcade.load_texture("questions/sec6.png")
        arcade.draw_scaled_texture_rectangle(WIDTH/2,HEIGHT/2, texture,1,0) 

    def on_key_press(self, key, _modifiers):
        if key != arcade.key.RIGHT and key != arcade.key.LEFT and key != arcade.key.UP and key != arcade.key.DOWN:
            if key != arcade.key.D:
                game_over = GameOverView()
                game_over.total_time = self.total_time
                self.window.show_view(game_over)
            else:
                self.window.show_view(self.game_view)

class GamePauseView7(arcade.View):
    def __init__(self, game_view):
        super().__init__()
        self.game_view = game_view
        self.total_time = 0
    
    def on_draw(self):
        arcade.start_render()
        texture = arcade.load_texture("questions/sec7.png")
        arcade.draw_scaled_texture_rectangle(WIDTH/2,HEIGHT/2, texture,1,0) 

    def on_key_press(self, key, _modifiers):
        if key != arcade.key.RIGHT and key != arcade.key.LEFT and key != arcade.key.UP and key != arcade.key.DOWN:
            if key != arcade.key.A:
                game_over = GameOverView()
                game_over.total_time = self.total_time
                self.window.show_view(game_over)
            else:
                self.window.show_view(self.game_view)
        
class GamePauseView8(arcade.View):
    def __init__(self, game_view):
        super().__init__()
        self.game_view = game_view
        self.total_time = 0
    
    def on_draw(self):
        arcade.start_render()
        texture = arcade.load_texture("questions/sec8.png")
        arcade.draw_scaled_texture_rectangle(WIDTH/2,HEIGHT/2, texture,1,0) 

    def on_key_press(self, key, _modifiers):
        if key != arcade.key.RIGHT and key != arcade.key.LEFT and key != arcade.key.UP and key != arcade.key.DOWN:
            if key != arcade.key.D:
                game_over = GameOverView()
                game_over.total_time = self.total_time
                self.window.show_view(game_over)
            else:
                self.window.show_view(self.game_view)


def main():

    window = arcade.Window(WIDTH, HEIGHT, "MY BEAUTIFUL GAME")
    menu_view = MenuView()
    window.show_view(menu_view)
    arcade.run()
    

if __name__ == "__main__":
    main()
