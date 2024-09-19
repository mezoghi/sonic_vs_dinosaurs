import pyglet
from pyglet.window import key
from game import Game
from constants import *

window = pyglet.window.Window(width=1000, height=500, caption="Endless Runner Game")

batch = pyglet.graphics.Batch()

background_image = pyglet.image.load_animation('assest/_bc.gif')
background = pyglet.sprite.Sprite(background_image, x=0, y=0)

ground = pyglet.shapes.Rectangle(0, 50, 1000, 20, color=(0, 0, 255), batch=batch)

jump_sound = pyglet.media.load('assest/jump-and-spark-6136.mp3', streaming=False)
game_over_sound = pyglet.media.load('assest/game-over-arcade-6435.mp3', streaming=False)

game = Game(window, batch, ground, jump_sound, game_over_sound)

@window.event
def on_key_press(symbol, modifiers):
    if symbol == key.SPACE:
        if game.state == 'start':
            game.start_game()
        elif game.state == 'playing':
            game.player.jump()
    if symbol == key.DOWN:
        game.player.crouch()  
    if symbol == key.LSHIFT or symbol == key.RSHIFT:
        game.player.activate_invincibility()  
    if symbol == key.R and game.state == 'game_over':
        game.reset_game()

@window.event
def on_key_release(symbol, modifiers):
    if symbol == key.DOWN:
        game.player.stand_up()
    if symbol == key.LSHIFT or symbol == key.RSHIFT:
        game.player.deactivate_invincibility() 
def update(dt):
    game.update(dt)

@window.event
def on_draw():
    window.clear()
    background.draw() 
    game.draw()  
pyglet.clock.schedule_interval(update, 1/60.0)

pyglet.clock.schedule_interval(lambda dt: game.create_obstacle(), 1.5)

pyglet.app.run()
