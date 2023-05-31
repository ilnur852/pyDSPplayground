import numpy as np
import matplotlib.pyplot as plt

def downsapmle(signal, factor):
    i =0
    out = []
    while i < len(signal):
        out = np.append(out, signal[i])
        i+= int(np.floor(factor))
    return out


def Farrow_interpolator(signal, Q, P, x0):
    
    k = 0
    s = np.zeros(4)
    n =0
    a0 =0
    a1 =0
    a2 =0
    a3 =0
    deltak =0
    xk =0
    yk = np.array(0)
    sig = np.append(np.zeros(4), signal)
    Ns = len(signal)
    if (Q>=P):
        R = Ns/(Q/P)
    else: 
        R= (Ns-1)*P +1

    for k in range(int(R)):
        xk = k*(Q/P) - x0
        n= int(np.floor(xk)) + 1
        deltak = np.floor(xk) + 1- xk
        s[0:3] = sig[n:n+3]
        a0 = s[2]
        a3 = (1/6)*(s[3] - s[0]) + (1/2)*(s[1]- s[2])
        a1 = (1/2)*(s[3] - s[1]) - a3
        a2 = s[3] - s[2] - a1 - a3
        res = a0 - deltak*(a1 - deltak*(a2 - deltak*a3))
        yk = np.append(yk, res)
    return yk


if __name__=='__main__':
    
    N  = 12
    sw = np.sin(np.linspace(0, 4*np.pi , N))
    swd= downsapmle(sw, 16)
    ipsw_nodelay = Farrow_interpolator(sw, 1, 16, 0)
    ipsw_delay = Farrow_interpolator(sw, 1, 16, -1)   

    plt.subplot(3,1,1)
    plt.stem(sw)
    plt.grid(True)
    plt.subplot(3,1,2)
    plt.stem(ipsw_nodelay)
    plt.grid(True)
    plt.subplot(3,1,3)
    plt.stem(ipsw_delay)
    plt.grid(True)
    plt.show()
