import numpy as np
import matplotlib.pyplot as plt
import math

def sig(t):
    return 1/(1+math.e**t)

def derivative_sig(t):
    s = sig(t)
    return s+(1-s)

def softmax(t):
    out = np.exp(t)
    return out / np.sum(out)

def sparse_cross_entropy(z, y):
    return -np.log(z[0, y])

def to_full(y, num_classes):
    y_full = np.zeros((1, num_classes))
    y_full[0, y] = 1
    return y_full


ALPHA = 0.0004
TIMES = 10000

class ANN():
    def __init__(self, settings):
        self.loss_arr = []
        self.input_dim, self.h_dim, self.output_dim = settings
        self.w1 = np.random.randn(self.input_dim, self.h_dim)
        self.b1 = np.random.randn(1, self.h_dim)
        self.w2 = np.random.randn(self.h_dim, self.output_dim)
        self.b2 = np.random.randn(1, self.output_dim)


    def predict(self, x):
        self.x = x
        self.t1 = self.x @ self.w1 + self.b1
        self.h1 = sig(self.t1)
        self.t2 = self.h1 @ self.w2 + self.b2
        self.z = softmax(self.t2)
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
        de_dw2 = self.h1.T @ de_dt2
        de_db2 = de_dt2
        de_dh1 = de_dt2 @ self.w2.T
        de_dt1 = de_dh1 * derivative_sig(self.t1)
        de_dw1 = self.x.T @ de_dt1
        de_db1 = de_dt1

        self.w1 = self.w1 - ALPHA*de_dw1
        self.b1 = self.b1 - ALPHA*de_db1
        self.w2 = self.w2 - ALPHA*de_dw2
        self.b2 = self.b2 - ALPHA*de_db2

    def show_progress(self, arr = 0):
        if type(arr)==int:
            arr = self.loss_arr
        plt.plot(arr)
        plt.show()