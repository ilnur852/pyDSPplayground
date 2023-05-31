import numpy as np
import matplotlib.pyplot as plt
from scipy import linalg as la

N = 32
p = 1
sRate = 128

ovs = sRate * N
#vars 
pi = np.pi

#generate sequence
t = np.linspace(0, 2*pi, num=N)
x =  np.sin(2*np.pi * t) + np.random.random(N) * 0.3

plt.plot(x)
plt.show()

#find autocorrelations
conj = np.conj(x)
flip = conj[::-1] 
acf =  np.convolve(x, flip) #autocorrelation function - convotution of time reversal of self

#construct autocorrelation matrix (Toeplitz)
Rxx = la.toeplitz(acf)

#eigendecomposition of Rxx
v, d = la.eig(Rxx) # v- eigenvalues , d - corresponding eigenvectors 

indexes = np.argsort(v)[::-1]
sort_eigvals = v[indexes] # sorting eigenvalues from greatest to least (retr)
sort_eigvects = d[:, indexes]

#separating signal and noise subspace eigenvectors
signal_eigvects = sort_eigvects[0:p]
noise_eigvects = sort_eigvects[p:len(sort_eigvects)]

#print ("Signal\n", signal_eigvects)
#print ("Noise\n", noise_eigvects)
print("length noise eigenvector", len(noise_eigvects), len(noise_eigvects[0]))

#perform MUSIC frequency estimation
Pmu = []
for k in range(0, ovs + 1):
    sum1 = 0
    sum2 = 0
    freq_vector = np.zeros(len(noise_eigvects[0]), dtype=np.complex_)

    f = float(k)/ovs

    for i in range(0, len(noise_eigvects[0])):
        freq_vector[i] = np.conjugate(complex(np.cos(2 * pi* i * f), np.sin(2 * pi * i *f))) # steering vector e definition
        #freq_vector[i] = np.conjugate(np.exp(1j*i*f))

    for u in range(0, len(noise_eigvects)):
        sum1 += (abs(np.dot(np.asarray(freq_vector).transpose(), np.asarray(noise_eigvects[u]))))**2 # |e^H * vk|^2

    #print(f, 1/sum)
    Pmu = np.append(Pmu, 1/sum1)

    #sum2 += np.fft.fft(noise_eigvects[:, k], 1024)

plt.plot(Pmu)
plt.show()