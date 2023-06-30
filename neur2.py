import numpy as np
import matplotlib.pyplot as plt
import math

def sig(t):
    #return 1/(1+np.power(math.e, t))
    x = t.copy()
    x[x<=0] = 0
    return x

def derivative_sig(t):
    '''s = sig(t)
    return s+(1-s)'''
    x = t.copy()
    x[x<=0] = 0
    x[x>0] = 1
    return x

def softmax(t):
    out = np.exp(t)
    return out / np.sum(out)

def sparse_cross_entropy(z, y):
    return -np.log(z[0, y])

def to_full(y, num_classes):
    y_full = np.zeros((1, num_classes))
    y_full[0, y] = 1
    return y_full


ALPHA = 0.03
TIMES = 10000

def gen_weights(columns, lines):
    return np.random.sample((columns, lines)).astype(np.longdouble)

class ANN():
    def __init__(self, settings):
        self.loss_arr = []
        self.input_dim, self.h_dim, self.h2_dim, self.output_dim = settings
        self.w1 =  gen_weights(self.input_dim, self.h_dim)
        self.b1 =  gen_weights(1, self.h_dim)
        self.ww =  gen_weights(self.h_dim, self.h2_dim)
        self.bb =  gen_weights(1, self.h2_dim)
        self.w2 =  gen_weights(self.h2_dim, self.output_dim)
        self.b2 =  gen_weights(1, self.output_dim)


    def predict(self, x):
        self.x = x
        self.t1 = self.x @ self.w1 + self.b1
        self.h1 = sig(self.t1)
        self.tt = self.h1 @ self.ww + self.bb
        self.hh = sig(self.tt)
        self.t2 = self.hh @ self.w2 + self.b2
        self.z = softmax(self.t2)
        '''with open('file.txt', 'a+') as f:
            f.write('\n')
            f.write('w1 max {0}\n'.format(self.w1.max()))
            f.write('w2 max {0}\n'.format(self.w2.max()))
            f.write('ww max {0}\n'.format(self.ww.max()))
            f.write('w1 min {0}\n'.format(self.w1.min()))
            f.write('w2 min {0}\n'.format(self.w2.min()))
            f.write('ww min {0}\n'.format(self.ww.min()))
            f.write('b1 max {0}\n'.format(self.b1.max()))
            f.write('b1 min {0}\n'.format(self.b1.min()))
            f.write('bb max {0}\n'.format(self.bb.max()))
            f.write('bb min {0}\n'.format(self.bb.min()))'''
        out = np.argmax(self.z)
        return out

    def calculate_error(self, y):
        self.y = y
        self.E = sparse_cross_entropy(self.z, self.y)
        self.loss_arr.append(self.E)

    def back_prop(self, y):
        if type(y) == np.int64:
            y_full = to_full(y, self.output_dim)
        else:
            g = np.array(y)
            y_full = g.reshape((1, self.output_dim))
        de_dt2 = self.z-y_full
        de_dw2 = self.hh.T @ de_dt2
        de_db2 = de_dt2
        de_dhh = de_dt2 @ self.w2.T
        de_dtt = de_dhh * derivative_sig(self.tt)
        de_dww = self.h1.T @ de_dtt
        de_dbb = de_dtt
        de_dh1 = de_dtt @ self.hh.T
        de_dt1 = de_dh1 * derivative_sig(self.t1)
        de_dw1 = self.x.T @ de_dt1
        de_db1 = de_dt1

        self.w1 = self.w1 - ALPHA*de_dw1
        self.b1 = self.b1 - ALPHA*de_db1
        self.ww = self.ww - ALPHA*de_dww
        self.bb = self.bb - ALPHA*de_dbb
        self.w2 = self.w2 - ALPHA*de_dw2
        self.b2 = self.b2 - ALPHA*de_db2

    def show_progress(self, arr = 0):
        if type(arr)==int:
            arr = self.loss_arr
        plt.plot(arr)
        plt.show()