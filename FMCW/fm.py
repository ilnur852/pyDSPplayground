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

N = int(1e4)
t = np.linspace(0, 50, N)
a = 0.2

tri_shape1 = triagshape(t, a, 0.02, 0.40)
tri_shape2 = triagshape(t, a, 0.65, .40)
tri_shape3 = triagshape(t, a*.8, 0.552, .41)
tri_shape4 = triagshape(t, a*.6, 0.555, .41)

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
mixed = s1*s2 + s1*s3 + s1*s4
'''
plt.plot(mixed)
plt.show()
'''
b = firwin(64, 0.1)
mixfilt = np.convolve(b, mixed)

h, Pxx = periodogram(mixfilt, N, 'flattop', scaling='spectrum')

plt.semilogy(h, Pxx)
plt.ylim([1e-4, 1e0])
plt.show()

pulse = mixfilt >0

i = 0
acc = np.zeros(len(pulse))
da = np.zeros(len(pulse))

for i in range(len(pulse)-1):
    if pulse[i+1] == pulse[i]:
        acc[i] = 0
    else:
        acc[i] = 1
    
i = 0
for i in range(len(acc)):
    da[i] = np.sum(acc[i:i+3142*2])

plt.subplot(411)
plt.plot(tri_shape1)
plt.subplot(412)
plt.plot(mixfilt)
plt.subplot(413)
plt.plot(acc)
plt.subplot(414)
plt.plot(da)
plt.show()

l= int(len(da))
print(np.mean(da))

tri_per = (N/20)*2*np.pi
print("triangle period", tri_per)

b = firwin(256, 0.001)
mixfilt_low = np.convolve(b, mixed)

plt.subplot(211)
plt.plot(mixfilt_low)
plt.subplot(212)
plt.plot(tri_shape1)
plt.show()
