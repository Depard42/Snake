import numpy as np
import time

SIZE = np.array([5,5])
block_size = 40
Map = np.zeros(SIZE).astype(int)
human = __name__ == '__main__'
steps = 0
score_arr = []

def map_reset():
    global Map
    Map = np.zeros(SIZE).astype(int)

class Snake():
    def __init__(self):
        self.reset()
    
    def change_dir(self, dir_num):
        if not self.is_change_dir:
            if dir_num == 0: #top
                dir = np.array([0,-1])
            elif dir_num == 1: #bottom
                dir = np.array([0,1])
            elif dir_num == 2: #left
                dir = np.array([-1,0])
            else: #right
                dir = np.array([1,0])
            if not np.array_equal(dir+self.cur_dir, [0,0]): #направление не противоположно текущему?
                self.cur_dir = dir
            self.is_change_dir = True
    
    def move(self):
        self.is_change_dir = False
        new_coord = self.xy + self.cur_dir
        if 0 <= new_coord[0] < SIZE[0] and 0 <= new_coord[1] < SIZE[1] and Map[*new_coord] != 1:
            self.xy += self.cur_dir
            self.body.append(self.xy.copy())
            if Map[*self.xy] == 2:
                self.score += 1
                self.len += 1
                self.create_Apple()
                self.state = 1
            else:
                Map[*self.body.pop(0)] = 0
                self.state = 0
            Map[*self.xy] = 1
        else:
            if human:
                time.sleep(1)
            state = 2
            score_arr.append(self.score)
            self.reset()
    
    def create_Apple(self):
        while 1:
            self.apple = np.random.randint(0,SIZE[0],2)
            if Map[*self.apple] == 1:
                continue
            Map[*self.apple] = 2
            break
    
    def reset(self):
        map_reset()
        self.xy = np.array([SIZE[0]//2,SIZE[1]//2]) 
        self.cur_dir = np.array([0,1])
        self.len = 1
        self.score = 0
        self.is_change_dir = False
        Map[*self.xy] = 1
        self.body = [self.xy.copy()]
        self.create_Apple()
        self.state = 0 # 0 is normal, 1 eat apple, 2 is crash
    
    def apple_dist(self): #for agent
        return np.sum((self.xy-self.apple)**2)**(1/2)


import pygame as pg
pg.init()
scr = pg.display.set_mode(SIZE*block_size + [0, 80])
pg.font.init()
font = pg.font.SysFont('Comic Sans Ms', 30)
snake = Snake()
stop = False

def show():
    for event in pg.event.get():
        if event.type == pg.QUIT:
            return 1
        elif event.type == pg.KEYDOWN and human:
            if event.key == pg.K_UP:
                snake.change_dir(0)
            elif event.key == pg.K_DOWN:
                snake.change_dir(1)
            elif event.key == pg.K_LEFT:
                snake.change_dir(2)
            elif event.key == pg.K_RIGHT:
                snake.change_dir(3)
    snake.move()
    
    scr.fill((255,255,255))
    for i in range(SIZE[0]):
        for j in range(SIZE[1]):
            pg.draw.rect(scr, ((i*30) % 150+105,(i*j*60) % 150+105,(j*30*40) % 150+105), (i*block_size,j*block_size,block_size,block_size))
    score_text = font.render("score {0}".format(snake.score), False, (0, 0, 0))
    scr.blit(score_text, (3, SIZE[1]*block_size))
    steps_text = font.render("step {0}".format(steps), False, (0, 0, 0))
    scr.blit(steps_text, (3, SIZE[1]*block_size+50))
    for i in range(len(snake.body)):
        pg.draw.rect(scr, (105+150//(i/3+1),0,0), np.hstack([snake.body[-i-1]*block_size, [block_size, block_size]]))
    pg.draw.circle(scr, (33,66,30), snake.apple * block_size + block_size//2, block_size//2)
    pg.display.update()
    return 0

if human:
    while not stop:
        stop = show()
        pg.time.delay(400)

'''
while not stop:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            stop = True
        elif event.type == pg.KEYDOWN and human:
            if event.key == pg.K_UP:
                snake.change_dir(0)
            elif event.key == pg.K_DOWN:
                snake.change_dir(1)
            elif event.key == pg.K_LEFT:
                snake.change_dir(2)
            elif event.key == pg.K_RIGHT:
                snake.change_dir(3)
    if human or can_go:
        snake.move()
    else:
        continue
    scr.fill((255,255,255))
    for i in range(SIZE[0]):
        for j in range(SIZE[1]):
            pg.draw.rect(scr, ((i*30) % 150+105,(i*j*60) % 150+105,(j*30*40) % 150+105), (i*block_size,j*block_size,block_size,block_size))
    score_text = font.render("score {0}".format(snake.score), False, (0, 0, 0))
    scr.blit(score_text, (3, SIZE[1]*block_size))
    for i in range(len(snake.body)):
        pg.draw.rect(scr, (105+150//(i/3+1),0,0), np.hstack([snake.body[-i-1]*block_size, [block_size, block_size]]))
    pg.draw.circle(scr, (33,66,30), snake.apple * block_size + block_size//2, block_size//2)
    pg.display.update()

    if human:
        pg.time.delay(400)
    else:
        can_go = False

'''