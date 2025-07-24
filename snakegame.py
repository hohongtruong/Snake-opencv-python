import cv2
import numpy as np
import time

class SnakePart:
    def __init__(self, h, w, is_head = True,stand_still = False):
        self.h = h
        self.w = w
        self.is_head = is_head
        self.image = self.gen_image()
        self.next_part = None
        self.stand_still = stand_still

    def get_dot(self):
        dot_color = (0, 75, 150)
        dot = np.full((3,3,3), dot_color, np.uint8)
        return dot
    
    def gen_image(self):
        head_color = (118, 66, 78)
        head_image = np.full((10,10,3), head_color, np.uint8)
        if self.is_head:
            return head_image
        body_color = (0,255,0)
        body_image = np.full((10,10,3), body_color, np.uint8)
        for _ in range(3):
            dot_pos_w = np.random.randint(0,7)
            dot_pos_h = np.random.randint(0,7)
            body_image[dot_pos_h:dot_pos_h+3,dot_pos_w:dot_pos_w+3] = self.get_dot()
        return body_image
    
    def move(self,h,w):
        if self.stand_still:
            self.stand_still = False
            return
        if self.next_part:
            self.next_part.move(self.h,self.w)
        self.h = h
        self.w = w

    def move_up(self):
        self.move(self.h-1,self.w)
    
    def move_down(self):
        self.move(self.h+1,self.w)

    def move_left(self):
        self.move(self.h,self.w-1)

    def move_right(self):
        self.move(self.h,self.w+1)
    
    def normalize(self, max_h, max_w):
        self.h %= max_h//10
        self.w %= max_w//10

    def add_part(self):
        new_part = SnakePart(self.h,self.w,is_head = False,stand_still=True)
        if self.next_part is None:
            self.next_part = new_part
            return
        part = self.next_part
        while part.next_part is not None:
            part = part.next_part
        part.next_part = new_part

    def render(self,image):
        if self.next_part:
            self.next_part.render(image)
        image[self.h*10:(self.h+1)*10, self.w*10:(self.w+1)*10] = self.image
    
    def collision(self):
        part = self.next_part
        while part:
            if part.w == self.w and part.h == self.h:
                return True
            part = part.next_part
        return False
    
    
class Snake:
    def __init__(self, maxh, maxw):
        self.maxh = maxh
        self.maxw = maxw
        h = np.random.randint(0,self.maxh//10)
        w = np.random.randint(0,self.maxw//10)
        self.key = 2555904
        self.snake_head = SnakePart(h,w,is_head=True)

    def move(self, key):
        if self.valid_key(key):
            self.key = key
        
        key_map = {2490368:self.snake_head.move_up,
                   2621440:self.snake_head.move_down,
                   2555904:self.snake_head.move_right,
                   2424832:self.snake_head.move_left}
        key_map[self.key]()
        self.snake_head.normalize(self.maxh, self.maxw)
    
    def grownth(self):
        self.snake_head.add_part()

    def valid_key(self,key):
        return key == 2490368 and self.key!=2621440 or key == 2621440 and self.key!=2490368 or key == 2424832 and self.key!= 2555904 or key == 2555904 and self.key!= 2424832

    def render(self,image):
        self.snake_head.render(image)
    
    def self_collision(self):
        return self.snake_head.collision()
    
    def get_list_postion(self):
        pos = [(self.snake_head.h, self.snake_head.w)]
        part = self.snake_head.next_part
        while part:
            pos.append((part.h, part.w))
            part = part.next_part
        return pos
    
    def get_head_pos(self):
        return self.snake_head.h, self.snake_head.w

class Apple:
    color = (0,0,255)
    apple_image = np.full((10,10,3), (0,0,255), np.uint8)
    def __init__(self, maxh, maxw):
        self.maxh = maxh
        self.maxw = maxw
        self.init_pos()

    def render(self,image):
        image[self.h*10:(self.h+1)*10,self.w*10:(self.w+1)*10] = self.apple_image

    def init_pos(self, not_spawn =[]):
        self.h = np.random.randint(0,self.maxh//10)
        self.w = np.random.randint(0,self.maxw//10)
        while (self.w,self.h) in not_spawn:
            self.h = np.random.randint(0,self.maxh//10)
            self.w = np.random.randint(0,self.maxw//10)
    
    def get_pos(self):
        return self.h, self.w

class SnakeGame:
    def __init__(self, height = 400, width = 600):
        self.height = height
        self.width = width
        self.backgound_color = np.full((height, width, 3), (255, 255, 255), np.uint8)

        self.snake = Snake(self.height, self.width)
        self.apple = Apple(self.height, self.width)

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
            
            if self.snake.get_head_pos() == self.apple.get_pos():
                self.snake.grownth()
                self.apple.init_pos(not_spawn = self.snake.get_list_postion())
                self.score += 1

            self.apple.render(image)
            self.snake.render(image)
            image = self.text_render(image,self.score)
            cv2.imshow("Snake", image)
            key = cv2.waitKeyEx(200)
            self.snake.move(key)
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