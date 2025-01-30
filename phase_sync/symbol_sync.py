import numpy as np
import matplotlib.pyplot as plt
from rcosf import raised_root_cosine as rrc
from carr_sync import carrier_sync as cs

def symsync(signal, K1, K2, sps):
    symcnt = 0
    strobe = 0
    strobecnt = 1
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

    #output append
    for i in range(len(signal)-sps):
        # gemerate strobes for timing error buffer 
        if (symcnt <= 0):
            strobe = 1
        else: 
            symcnt = symcnt -1
            strobe =0
        # TED buffer  
        if (strobe):
            #complex to real imag conversion
            xk_d2 = np.real(signal[i+sps])
            xk_d1 = np.real(signal[i+sps//2])
            xk = np.real(signal[i])
            #previous sample
            yk_d2 = np.imag(signal[i+sps])
            yk_d1 = np.imag(signal[i +sps//2])
            yk = np.imag(signal[i])
            #calculate error using Gardner error detector
            #Loop filter
            #update counter offset value

            if strobecnt == 1:
                strobecnt = 0
                ek = xk_d1 * (xk_d2 -xk) + yk_d1 * (yk_d2 - yk)
                vp = K1*ek
                vi = vi + K2*ek
                vn = vp + vi
                out = np.append(out, (xk + 1j*yk))
                ev = np.append(ev, vn)
            else: strobecnt = strobecnt + 1
            symcnt = sps/2 -1 - vn
            
    return out , ev

def symsync_lgc(signal, Bn, dn, sps):
    cs_inst= cs()  
    K1, K2 = cs_inst.calcloopgains(Bn, dn, sps)
    return symsync(signal, K1, K2, sps)

def selsample(signal, sps, delay):
    n= 0
    ov = []
    while (n < len(signal) - sps):
        ok = signal[n+delay]
        n = n + sps
        ov = np.append(ov, ok)
    return ov

if __name__ == "__main__":
    
    num_symbols = 1999
    ev =[0, 0]
    N = 64*num_symbols
    # Crate random samples
    x_int = np.random.randint(0, 8, num_symbols)  # 0 to 
    #x_int = np.array([3,6,8,1,4,5,4,7,1,2,3,0,2,6,3,2,7,1,3,4])
    x_degrees = x_int * 360 / 8.0   # //calculate phase shift degrees for each symbol
    x_radians = x_degrees * np.pi / 180.0  # sin() and cos() takes in radians
    x_symbols = np.cos(x_radians) + 1j * np.sin(x_radians)  # this produces our PSK complex symbols
    

    i = 0
    symbols = np.zeros(0)
    for i in range(num_symbols):
        symbols = np.append(symbols, np.ones(int(N / num_symbols)) * x_symbols[i])

    h = rrc(int(N / num_symbols), 1, 0.6)
    
    # addiotive noise
  
    
    bsbnd = np.convolve(h, symbols) 
    
    sps = int(len(bsbnd) / num_symbols)
    arr = np.zeros(176)
    
    bsbnd = np.append(arr, bsbnd) 
    n = 0.1*np.random.random(len(bsbnd))
    bsbnd = bsbnd/np.max(bsbnd) + n
    print (sps)
    
    ssbsnd, ev = symsync_lgc(bsbnd, 0.05, 0.707, sps)
    #select_only = selsample(bsbnd, sps, 14)

    print(len(ssbsnd))
    plt.title('sym synced')
    plt.plot(np.real(ssbsnd), np.imag(ssbsnd) , '.')
    plt.plot()
    plt.figure()
    plt.title('time error')
    plt.plot(ev)
    plt.show()
