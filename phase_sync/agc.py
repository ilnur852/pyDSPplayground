from tkinter import Y
import numpy as np
import matplotlib.pyplot as plt
from rcosf import raised_root_cosine

def linear_gc(xi, xq, sps, desired_lvl, alpha):
    lout_acc = 0 
    i = 0
    sps = int(sps) 
    yi = np.zeros(len(xi)+1)
    yq = np.zeros(len(xq)+1)
    est_lvl = np.zeros(len(xi))
    lc= np.zeros(len(xi))
    mv =np.zeros(len(xi))
    for i in range(len(xi)):
        est_lvl[i] = np.abs(yi[i]) + np.abs(yq[i])
        yi[i+1] = xi[i]*lout_acc
        yq[i+1] = xq[i]*lout_acc
        lout = (desired_lvl - est_lvl[i])*alpha
        lout_acc = lout + lout_acc
        lc[i] = lout
    return yi, yq, lc

def logariphmic_gc(xi, xq, sps, desired_lvl, alpha):
    lout_acc = 1
    i = 0 
    sps = int(sps) 
    yi = np.zeros(len(xi)+1)
    yq = np.zeros(len(xq)+1)
    est_lvl = np.zeros(len(xi))
    lc= np.zeros(len(xi))
    mv =0

    lout = 1
    for i in range(len(xi)):
        est_lvl[i] = np.abs(yi[i]) + np.abs(yq[i])
        yi[i+1] = xi[i] * np.exp(lout_acc)
        yq[i+1] = xq[i] * np.exp(lout_acc)
        if (np.abs(est_lvl[i])>0): 
            lout = np.floor((np.log(desired_lvl + 1) - np.log(est_lvl[i]) + 1)*alpha)
        lout_acc = lout + lout_acc
        lc[i] = np.exp(lout_acc)
    return yi, yq, lc

if __name__ == "__main__":
    num_symbols = 200
    N = 20000

    # Crate random samples
    x_int = np.random.randint(0, 8, num_symbols)  # 0 to 
    #x_int = np.array([3,6,8,1,4,5,4,7,1,2,3,0,2,6,3,2,7,1,3,4])
    print(len(x_int))
    x_degrees = x_int * 360 / 8.0 + 22.5  # //calculate phase shift degrees for each symbol
    x_radians = x_degrees * np.pi / 180.0  # sin() and cos() takes in radians
    x_symbols = np.cos(x_radians) + 1j * np.sin(x_radians)  # this produces our PSK complex symbols

    i = 0
    symbols = np.zeros(0)
    for i in range(num_symbols):
        symbols = np.append(symbols, np.ones(int(N / num_symbols)) * x_symbols[i])

    h = raised_root_cosine(N/num_symbols, 3, 0.6)

    filts = np.convolve(h, symbols)
    dsQ = np.real(filts)
    dsI = np.imag(filts)
    #dsI = np.append(dsI, dsI/20)
    #dsQ = np.append(dsQ, dsQ/20)
    
    gI, gQ, lvl = linear_gc(dsI, dsQ, (N/num_symbols), 10, 0.00001)
    gIl, gQl, lvll = logariphmic_gc(dsI, dsQ, (N/num_symbols), 10, 0.01)
    
    plt.subplot(611)
    plt.plot(dsQ)
    plt.subplot(612)
    plt.plot(dsI)
    plt.subplot(613)
    plt.ylim(-20, 20)
    plt.plot(gI)
    plt.subplot(614)
    plt.ylim(-25, 25)
    plt.plot(gQ)
    plt.subplot(615)
    plt.ylim(-25, 25)
    plt.plot(gQl)
    plt.subplot(616)
    plt.ylim(-25, 25)
    plt.plot(gIl)
    plt.show()

    plt.subplot(121)
    plt.plot(lvl)
    plt.subplot(122)
    plt.plot(lvll)
    plt.show()
    
    plt.scatter(gI, gQ)
    plt.show()
