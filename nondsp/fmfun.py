import numpy as np
from scipy.signal import sawtooth

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
