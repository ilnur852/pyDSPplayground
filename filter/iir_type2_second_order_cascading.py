import numpy as np
import matplotlib.pyplot as plt
from scipy import signal

def t2_iir(x ,a, b, order):
    xz = np.zeros(order+1) # create 1-d array w/ size of order of filter
    y = []
    i = 0
    yk = 0
    w = 0
    for i in range(len(x)): #iteratevely output filter stages
        w = -np.dot(a[1:], xz[1:][::-1]) + x[i]
        yk= np.dot(b, xz[::-1])
        xz = np.append(xz[1:], w)
        y = np.append(y , yk)
    return y

def bin_repr_file_save(data, file, width):
    i=0
    for i in range(len(data)):
        fdat = np.floor(data[i]).astype(int)
        file.write((np.binary_repr(fdat, width=width) + "\n"))


if __name__=="__main__":
    with np.load("filtcoef.npz") as data:
        d = data['ba']
    a = d[: ,1]
    b = d[: ,0]
    a = a.astype(np.float32)
    b = b.astype(np.float32)
    print(a)
    print(b)
    x = np.linspace(0, 5, 1024)
    s  = np.sin(np.exp(x))
    outfile1 = open("sw.txt", "w")
    bin_repr_file_save(s*2**9, outfile1, 10)
    outfile1.close()
    
    fo = t2_iir(s , a, b, len(b)-1)
    fo_s = signal.lfilter(b,a,s)
    plt.subplot(311)
    plt.title('input sequence')
    plt.plot(s)
    plt.subplot(312)
    plt.title('filtered w/ custom implementation')
    plt.plot(fo)
    plt.subplot(313)
    plt.title('filtered using scipy lfilt')
    plt.plot(fo_s)
    plt.show()
