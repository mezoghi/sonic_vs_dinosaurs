import pyglet
from constants import *

class Player:
    def __init__(self, x, y, normal_image_path, crouch_image_path, invincibility_image_path, batch):
        self.normal_image = pyglet.image.load(normal_image_path)
        self.crouch_image = pyglet.image.load(crouch_image_path)
        self.invincibility_image = pyglet.image.load(invincibility_image_path)
        self.normal_image.width = 160
        self.normal_image.height = 160
        self.crouch_image.width = 160
        self.crouch_image.height = 160
        self.invincibility_image.width = 240
        self.invincibility_image.height = 160
        self.sprite = pyglet.sprite.Sprite(self.normal_image, x=x, y=y, batch=batch)
        
        self.sprite.scale = 0.5  

        self.normal_scale = self.sprite.scale
        self.crouch_scale = self.sprite.scale
        self.invincibility_scale = self.sprite.scale

        self.velocity_y = 0 
        self.is_jumping = False  
        self.is_crouching = False  
        self.is_invincible = False

    def jump(self):
        if not self.is_jumping and not self.is_crouching:
            self.velocity_y = JUMP_SPEED  
            self.is_jumping = True  
           

    def crouch(self):
        if not self.is_jumping:
            self.is_crouching = True
            self.sprite.image = self.crouch_image 
            self.sprite.scale = self.crouch_scale  
            self.sprite.visible = True  

    def stand_up(self):
        if self.is_crouching:
            self.is_crouching = False
            if not self.is_invincible:
                self.sprite.image = self.normal_image 
                self.sprite.scale = self.normal_scale 
            self.sprite.visible = True 

    def activate_invincibility(self):
        self.is_invincible = True
        self.sprite.image = self.invincibility_image  
        self.sprite.scale = self.invincibility_scale  

    def deactivate_invincibility(self):
        self.is_invincible = False
        self.sprite.image = self.normal_image 
        self.sprite.scale = self.normal_scale 

    def apply_gravity(self, dt):
        if not self.is_crouching:
            self.velocity_y += GRAVITY * dt
            self.sprite.y += self.velocity_y * dt 

        if self.sprite.y <= GROUND_Y + GROUND_HEIGHT:
            self.sprite.y = GROUND_Y + GROUND_HEIGHT  
            self.velocity_y = 0 
            self.is_jumping = False 

    def reset(self):
        self.sprite.y = GROUND_Y + GROUND_HEIGHT
        self.velocity_y = 0
        self.is_jumping = False
        self.is_crouching = False
        self.is_invincible = False 
        self.sprite.image = self.normal_image 
        self.sprite.scale = self.normal_scale  
        self.sprite.visible = True 
