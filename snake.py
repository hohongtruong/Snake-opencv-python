import cv2
import numpy as np
import time

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
class SnakeGame:
    def __init__(self, height = 400, width = 600):
        self.height = height
        self.width = width
        self.backgound_color = np.full((height, width, 3), (255, 255, 255), np.uint8)
        grid_pos = [[(h,w) for h in range(0,height,10)] for w in range(0,width,10)]
        self.grid_pos = np.array(grid_pos)

        self.snake = Snake(self.grid_pos)
        self.apple = Apple(self.grid_pos)

        self.score = 0

    def text_render(self,image,text):
        font = cv2.FONT_HERSHEY_SIMPLEX
        org = (0, 25)
        fontScale = 1
        color = (255, 0, 0)
        thickness = 2
        return cv2.putText(image, str(text), org, font, fontScale, color, thickness, cv2.LINE_AA)

    def run(self):
        while True:
            image = self.backgound_color.copy()
            grownth = self.snake.w == self.apple.w and self.snake.h == self.apple.h
            if self.snake.w == self.apple.w and self.snake.h == self.apple.h:
                self.apple.init_pos(not_spawn = self.snake.snake_part)
                self.score += 1
            
            self.apple.render(image)
            self.snake.render(image)
            image = self.text_render(image,self.score)
            cv2.imshow("Snake", image)
            key = cv2.waitKeyEx(200)
            self.snake.move(key,grownth)
            if self.snake.self_collision():
                image = self.backgound_color.copy()
                self.apple.render(image)
                self.snake.render(image)
                image = self.text_render(image,"Game Over")
                cv2.imshow("Snake", image)
                cv2.waitKey(0)
                time.sleep(1)
                cv2.destroyAllWindows()
                break
            if key  == ord('q'): # Detect 'q' to quit
                cv2.destroyAllWindows()
                break

game = SnakeGame()
game.run()