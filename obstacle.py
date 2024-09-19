import pyglet

class Obstacle:
    def __init__(self, x, y, image_path, is_flying, batch):
        self.image = pyglet.image.load(image_path)
        self.sprite = pyglet.sprite.Sprite(self.image, x=x, y=y, batch=batch)
        
        if is_flying:
            self.sprite.scale = 0.4  
        else:
            self.sprite.scale = 0.5  

        self.is_flying = is_flying 
        self.passed = False  

    def update(self, dt, speed):
        self.sprite.x -= speed * dt

    def is_off_screen(self):
        return self.sprite.x + self.sprite.width < 0

    def check_collision(self, player):
        
        if player.is_crouching and self.is_flying:
            return False
        
        return (
            player.sprite.x + player.sprite.width > self.sprite.x and
            player.sprite.x < self.sprite.x + self.sprite.width and
            player.sprite.y < self.sprite.y + self.sprite.height
        )
