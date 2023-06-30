import neur2 as neur
import snake_env as env
import numpy as np
import pygame
import matplotlib.pyplot as plt
import matplotlib.animation as animation

VIEW_DIST = 1
#INPUT = env.SIZE[0]*env.SIZE[1]+2
INPUT = (VIEW_DIST*2+1)**2
H_DIM = 40
HH_DIM = 10
ann = neur.ANN((INPUT, H_DIM, HH_DIM, 4))

#grafic
fig, axs = plt.subplots(2)
axs[0].set_title('score')
axs[0].plot(env.score_arr)
axs[1].set_title('steps')
axs[1].plot(env.step_arr[:-1])
def animate():
    axs[0].clear()
    axs[1].clear()
    axs[0].set_title('score')
    axs[0].plot(env.score_arr)
    axs[1].set_title('steps')
    axs[1].plot(env.step_arr[:-1])
    plt.pause(0.01)
#plt.ion()
#plt.show(block=False)



while 1:
    add_border = np.pad(env.Map, pad_width=1, mode='constant',
               constant_values=1)
    add_view = np.pad(add_border, pad_width=VIEW_DIST-1, mode='constant',
               constant_values=0)
    sx, sy = env.snake.xy
    snake_view = add_view[sx:sx+2*VIEW_DIST+1,sy:sy+2*VIEW_DIST+1]
    x = neur.softmax(snake_view.flatten()).reshape(1,INPUT)
    predict = ann.predict(x)
    dir_check = (predict == env.snake.dir_num)
    env.snake.change_dir(predict)
    old_dist = env.snake.apple_dist()
    is_finish = env.show()
    new_dist = env.snake.apple_dist()

    if env.steps - env.step_arr[-1] >= 200:
        env.snake.looser()
    state = env.snake.state
    if state == 0 and not dir_check: # normal
        if old_dist > new_dist:
            y = [0.0333]*4
            y[predict] = 9
        else:
            y = [0.266]*4
            y[predict] = 0.2
    elif state == 1: #eat
        ann.back_prop(predict)
    else: #crash
        y = [0.33]*4
        y[predict] = 0
        ann.back_prop(y)
    
    if env.steps % 5000 == 0:
        print(env.steps)
        animate()
        plt.draw()
    env.steps += 1 
    if env.steps > 500000:
        env.pg.time.delay(300)
        #print(env.snake.state)
    if is_finish:
        break


#plt.show()