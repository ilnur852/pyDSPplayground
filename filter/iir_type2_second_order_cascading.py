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
        w = np.dot(-a[1:], xz[1:][::-1]) + x[i]
        yk= np.dot(b, xz)
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

    t = np.linspace(0, 625/2, 625*128)
    s = 2**15*signal.chirp(t, f0=.01, f1=2, t1=625/16, method='linear')
    outfile1 = open("sw.txt", "w")
    bin_repr_file_save(s, outfile1, 16)
    outfile1.close()
    w ,h  = signal.freqz(b, a)

    #fo = t2_iir(s , a, b, len(b)-1)
    fo = signal.lfilter(b, a, s)

    plt.plot(w, 20 * np.log10(abs(h)), 'b')
    plt.ylabel('Amplitude [dB]', color='b')
    plt.xlabel('Frequency [rad/sample]')
    plt.grid()


    plt.figure()
    plt.subplot(211)
    plt.plot(s)
    plt.xlabel('t (sec)')
    plt.subplot(212)
    plt.title('filtered w/ custom implementation')
    plt.plot(fo)
    plt.show()
