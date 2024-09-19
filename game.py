import pyglet
from player import Player
from obstacle import Obstacle
from constants import *
import random

class Game:
    def __init__(self, window, batch, ground, jump_sound, game_over_sound):
        self.window = window
        self.batch = batch
        self.ground = ground
        self.jump_sound = jump_sound
        self.game_over_sound = game_over_sound
        self.player = Player(50, 100, 'assest/1-night.png', 'assest/2-night.png', 'assest\sonic.png', batch=batch)
        self.obstacles = []
        self.score = 0
        self.score_label = pyglet.text.Label(f'Score: {self.score}', font_name='Arial', font_size=24,
                                             x=window.width - 150, y=window.height - 50, anchor_x='center', anchor_y='center', batch=batch)
        self.state = 'start'
        self.start_label = pyglet.text.Label('Press SPACE to Start the Game', font_name='Arial', font_size=36,
                                             x=window.width // 2, y=window.height // 2, anchor_x='center', anchor_y='center', color=(255, 255, 255, 255))
        self.game_over_label = pyglet.text.Label('Game Over! Press R to Restart', font_name='Arial', font_size=36,
                                                 x=window.width // 2, y=window.height // 2, anchor_x='center', anchor_y='center', color=(255, 0, 0, 255))
        self.obstacle_speed = PLAYER_SPEED

    def start_game(self):
        self.state = 'playing'
        self.reset_game()

    def reset_game(self):
        self.player.reset()
        self.obstacles = []
        self.score = 0
        self.obstacle_speed = PLAYER_SPEED
        self.score_label.text = f'Score: {self.score}'
        self.state = 'playing'

    def update(self, dt):
        if self.state != 'playing':
            return

        self.player.apply_gravity(dt)

        if self.player.is_invincible:
            self.score += 5 
            self.obstacle_speed = 500
        else:
            for obstacle in self.obstacles:
                if obstacle.sprite.x + obstacle.sprite.width < self.player.sprite.x and not obstacle.passed:
                    self.score += 1
                    self.score_label.text = f'Score: {self.score}'
                    obstacle.passed = True
                    self.obstacle_speed += 5
                    
       # if self.score > 1000:
    # self.obstacle_speed += 50  # زيادة السرعة بمقدار 50

        for obstacle in self.obstacles:
            obstacle.update(dt, self.obstacle_speed)

        self.obstacles = [obstacle for obstacle in self.obstacles if not obstacle.is_off_screen()]

        if not self.player.is_invincible:
            for obstacle in self.obstacles:
                if obstacle.check_collision(self.player):
                    self.game_over_sound.play()
                    self.state = 'game_over'

    def draw(self):
        self.batch.draw()
        if self.state == 'start':
            self.start_label.draw()
        elif self.state == 'game_over':
            self.game_over_label.draw()

    def create_obstacle(self):
        if self.state == 'playing':
            if random.choice([True, False]):
                obstacle = Obstacle(self.window.width, self.ground.y + self.ground.height, 'assest/4-green.png', False, batch=self.batch)
            else:
                obstacle = Obstacle(self.window.width, self.ground.y + self.ground.height + 150, 'assest/3-pter_n.png', True, batch=self.batch)
            self.obstacles.append(obstacle)
