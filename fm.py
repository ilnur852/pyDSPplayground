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

tri_shape1 = triagshape(t, a, 0.02, 0.4)
tri_shape2 = triagshape(t, a, 0.55, .4)
tri_shape3 = triagshape(t, a*.9, 0.405, .42)

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

plt.plot(s1)
plt.show()

mixed = s1[int(N/4):]*s2[int(N/4):] #+ s1*s3
'''
plt.plot(mixed)
plt.show()
'''
b = firwin(64, 0.08)
mixfilt = np.convolve(b, mixed)

h, Pxx = periodogram(mixfilt, N, 'flattop', scaling='spectrum')

plt.semilogy(h, Pxx)
plt.ylim([1e-4, 1e0])
plt.show()

pulse = mixfilt >0

i = 0
acc0 = np.zeros(len(pulse))
acc1 = np.zeros(len(pulse))
da = np.zeros(len(pulse))

for i in range(len(pulse)-1):
    if pulse[i] == 1:
        acc0[i+1] = acc0[i] + 1
    else:
        acc0[i+1] = acc0[i] -1
    da[i] = np.abs(np.max(acc0[i:i+4096]) - np.min(acc0[i:i+4096]))


plt.subplot(411)
plt.plot(tri_shape1)
plt.subplot(412)
plt.plot(mixfilt)
plt.subplot(413)
plt.plot(pulse)
plt.subplot(414)
plt.plot(acc0)
plt.show()

plt.plot(da)
plt.show()

l= int(len(da))
print(np.mean(da[int(l/4):int(l-l/4)]))

tri_per = (N/20)*2*np.pi
print("triangle period", tri_per)
