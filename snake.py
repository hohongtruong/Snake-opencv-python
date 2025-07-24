import numpy as np

class Snake:
    color = (0,255,0)
    snake_image = np.full((10,10,3), (0,255,0), np.uint8)
    head_image = np.full((10,10,3), (118, 66, 78), np.uint8)
    def __init__(self, grid_pos):
        self.grid_pos = grid_pos
        self.w = np.random.randint(0,self.grid_pos.shape[0])
        self.h = np.random.randint(0,self.grid_pos.shape[1])
        self.key = 2555904
        self.snake_part = [(self.w,self.h)]
    def move(self, key, grownth = False):
        if self.valid_key(key):
            self.key = key
        if self.key  == 2490368: # Perform action for 'Up' arrow
            self.h -= 1
        elif self.key  == 2621440: # Perform action for 'Down' arrow
            self.h += 1
        elif self.key  == 2424832: # Perform action for 'Left' arrow
            self.w -= 1
        elif self.key  == 2555904:# Perform action for 'Right' arrow
            self.w += 1
        self.normalize()
        self.snake_part.append((self.w,self.h))
        if not grownth:
            self.snake_part.pop(0)

    def valid_key(self,key):
        return key == 2490368 and self.key!=2621440 or key == 2621440 and self.key!=2490368 or key == 2424832 and self.key!= 2555904 or key == 2555904 and self.key!= 2424832

    def normalize(self):
        self.w %= self.grid_pos.shape[0]
        self.h %= self.grid_pos.shape[1]

    def render(self,image):
        for w,h in self.snake_part:
            snake_h,snake_w = self.grid_pos[w,h]
            image[snake_h:snake_h+10,snake_w:snake_w+10] = self.snake_image
        image[snake_h:snake_h+10,snake_w:snake_w+10] = self.head_image
    
    def self_collision(self):
        return (self.w,self.h) in self.snake_part[:-1]