import numpy as np
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

input_dim = 2
output_dim = 2
h_dim = 3
ALPHA = 0.0002
TIMES = 10000

class ANN():
    def __init__(self):
        self.loss_arr = []

        #x = np.random.randn(1, input_dim)
        #y = 1

        self.w1 = np.random.randn(input_dim, h_dim)
        self.b1 = np.random.randn(1, h_dim)
        self.w2 = np.random.randn(h_dim, output_dim)
        self.b2 = np.random.randn(1, output_dim)


    def 
    t1 = x @ w1 + b1
    h1 = sig(t1)
    t2 = h1 @ w2 + b2
    z = softmax(t2)
    E = sparse_cross_entropy(z, y)
    loss_arr.append(E)

    y_full = to_full(y, output_dim)
    de_dt2 = z-y_full
    de_dw2 = h1.T @ de_dt2
    de_db2 = de_dt2
    de_dh1 = de_dt2 @ w2.T
    de_dt1 = de_dh1 * derivative_sig(t1)
    de_dw1 = x.T @ de_dt1
    de_db1 = de_dt1

    w1 = w1 - ALPHA*de_dw1
    b1 = b1 - ALPHA*de_db1
    w2 = w2 - ALPHA*de_dw2
    b2 = b2 - ALPHA*de_db2


    import matplotlib.pyplot as plt
    plt.plot(loss_arr)
    plt.show()