import numpy as np

class Apple:
    color = (0,0,255)
    apple_image = np.full((10,10,3), (0,0,255), np.uint8)
    def __init__(self, grid_pos):
        self.grid_pos = grid_pos
        self.init_pos()
    def render(self,image):
        apple_h,apple_w = self.grid_pos[self.w,self.h]
        image[apple_h:apple_h+10,apple_w:apple_w+10] = self.apple_image
    def init_pos(self, not_spawn =[]):
        self.w = np.random.randint(0,self.grid_pos.shape[0])
        self.h = np.random.randint(0,self.grid_pos.shape[1])
        while (self.w,self.h) in not_spawn:
            self.w = np.random.randint(0,self.grid_pos.shape[0])
            self.h = np.random.randint(0,self.grid_pos.shape[1])