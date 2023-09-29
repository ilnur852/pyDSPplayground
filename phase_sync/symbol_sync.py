import numpy as np
import matplotlib.pyplot as plt
from rcosf import raised_root_cosine as rrc
from carr_sync import carrier_sync as cs

def symsync(signal, K1, K2, sps):
    symcnt = sps/2
    strobe = 0
    ek = 0
    vn = 0
    vp = 0
    vi = 0
    out = []
    ev = []
    xk_d2 = 0
    xk_d1 = 0
    xk = 0
    yk_d2 = 0
    yk_d1 = 0
    yk = 0

    for i in range(len(signal)):
        # gemerate strobes for timing error buffer 
        if (symcnt <= 0):
            symcnt = 0
            strobe = 1
        else: 
            symcnt = symcnt -1
            strobe =0
        # TED buffer  
        if (strobe):
            #complex to real imag conversion
            xk_d2 = xk_d1
            xk_d1 = xk
            xk = np.real(signal[i])
            yk_d2 = yk_d1
            yk_d1 = yk
            yk = np.imag(signal[i])
            #calculate error using Gardner error detector
            ek = xk_d1*(xk_d2 - xk) + yk_d1*(yk_d2 - yk)
            #Loop filter
            vp = K1*ek
            vi = vi + K2*ek
            vn = vp + vi
            #update counter offset value
            symcnt = sps/2 - np.round(vn)
            #output append
            out = np.append(out, (xk + 1j*yk))
            ev = np.append(ev, ek)
    return out, ev

if __name__ == "__main__":
    
    num_symbols = 1000
    
    N = 32*num_symbols
    # Crate random samples
    x_int = np.random.randint(0, 8, num_symbols)  # 0 to 
    #x_int = np.array([3,6,8,1,4,5,4,7,1,2,3,0,2,6,3,2,7,1,3,4])
    x_degrees = x_int * 360 / 8.0 + 35  # //calculate phase shift degrees for each symbol
    x_radians = x_degrees * np.pi / 180.0  # sin() and cos() takes in radians
    x_symbols = np.cos(x_radians) + 1j * np.sin(x_radians)  # this produces our PSK complex symbols

    i = 0
    symbols = np.zeros(0)
    for i in range(num_symbols):
        symbols = np.append(symbols, np.ones(int(N / num_symbols)) * x_symbols[i])

    h = rrc(int(N / num_symbols), 1, 0.6)
    
    bsbnd = np.convolve(h, symbols)
    print (len(bsbnd))
    Bn = 0.005
    dn= 0.707
    sps = int(len(bsbnd) / num_symbols)

    cs_inst= cs()    
    K1, K2 = cs_inst.calcloopgains(Bn, dn, sps)
    print (K1, K2)
    ssbsnd, ev = symsync(bsbnd, K1, K2, sps)
    
    plt.plot(np.real(bsbnd), np.imag(bsbnd))
    plt.figure()
    plt.plot(np.real(ssbsnd), np.imag(ssbsnd))
    plt.plot()
    plt.figure()
    plt.plot(ev)
    plt.show()
