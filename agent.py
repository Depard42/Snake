import neur
import snake_env as env
import numpy as np

H_DIM = 50
INPUT = env.SIZE[0]*env.SIZE[1]+2
ann = neur.ANN((INPUT, H_DIM, 4))

while 1:
    x = np.concatenate((env.Map.flatten(), env.snake.xy)).reshape(1,INPUT)
    predict = ann.predict(x)
    env.snake.change_dir(predict)

    old_dist = env.snake.apple_dist()
    is_finish = env.show()
    new_dist = env.snake.apple_dist()

    state = env.snake.state
    if state == 0: # normal
        if old_dist > new_dist:
            y = [0.1]*4
            y[predict] = 0.8
        else:
            y = [0.2]*4
            y[predict] = 0.21
        ann.back_prop(y)
    elif state == 1: #eat
        ann.back_prop(predict)
    else: #crash
        y = [0.5]*4
        y[predict] = 0
        ann.back_prop(y)
    
    env.steps += 1 
    if env.steps > 999999:
        env.pg.time.delay(300)
    if is_finish:
        break
ann.show_progress(env.score_arr)