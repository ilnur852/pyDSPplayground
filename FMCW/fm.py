import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import *

#Returns integral of inpul array over N samples
def integrator(signal, N):
    phi = np.zeros(N)
    for i in range(len(signal)):
        phi[i] = phi[i-1]+ signal[i]
    return phi

#Creates triangular shaped signal using scipy.signal lib
def triagshape(t, amplitude, delay, freqoffset):
    return (sawtooth(t - delay, 0.5)+1)*amplitude+ freqoffset

#Creates FM modulated signal over N samples using quadrature modulation method
#For proper operation requires shape signal to be normalized 
def FMMOD(shape, N):
    return np.cos(integrator(shape, N)) + np.sin(integrator(shape, N))

if __name__ == "__main__":
    N = int(2**16)
    t = np.linspace(0, 100, N)
    a = 0.2
    Nfft =8192

    tri_shape1 = triagshape(t, a, 0.2, 0)
    tri_shape2 = triagshape(t, a, 1.5, 0)
    tri_shape3 = triagshape(t, a, 1.5, 0.0)
    tri_shape4 = triagshape(t, a*.6, 5.555, .41)

    plt.plot(tri_shape1)
    plt.plot(tri_shape2)
    #plt.plot(tri_shape3)
    plt.ylabel('Frequency')
    plt.xlabel('time (samples)')
    plt.legend(['сигнал 1','сигнал 2', 'сигнал 3'])
    plt.show()

    s1 = FMMOD(tri_shape1, N)
    s2 = FMMOD(tri_shape2, N)
    s3 = FMMOD(tri_shape3, N)
    s4 = FMMOD(tri_shape4, N)
    '''
    plt.plot(s1)
    plt.sho'w()
    '''
    mixed = s1*s2

    plt.plot(mixed)
    plt.show()

    b = firwin(256, 0.1)
    mixfilt = np.convolve(b, mixed)

    h, Pxx = periodogram(mixed, Nfft, 'boxcar', scaling='spectrum')
    mixed2= s1*s3 + 0.01*np.random.randn(N)
    h2, Pxx2 = periodogram(mixed2, Nfft, 'boxcar', scaling='spectrum')

    plt.semilogy(Pxx[1:5000])
    plt.semilogy(Pxx2[1:5000])
    plt.show()
