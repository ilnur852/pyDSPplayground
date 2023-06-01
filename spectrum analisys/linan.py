import numpy as np
import matplotlib.pyplot as plt
from scipy import linalg as la

N = 32
p = 4
sRate = 128

#vars 
pi = np.pi

#generate sequence
t = np.linspace(0, 2*pi, num=N)
x =  np.sin(8* t) + np.cos(4*t) + 0.1*np.random.random(N) 

plt.plot(x)
plt.show()

fft_x = abs(np.fft.fft(x, 128))

plt.plot(fft_x[:int(len(fft_x)/2)])

#find autocorrelations
conj = np.conj(x)
flip = conj[::-1] 
acf =  np.convolve(x, flip) #autocorrelation function - convotution of time reversal of self

#construct autocorrelation matrix (Toeplitz)
Rxx = la.toeplitz(acf)
Rxest = (1/len(x))*np.outer(np.asarray(x), np.asarray(conj))

#eigendecomposition of Rxx
v, d = np.linalg.eig(Rxx) # v- eigenvalues , d - corresponding eigenvectors 

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
'''
for k in range(0, ovs + 1):
    sum1 = 0
    sum2 = 0
    freq_vector = np.zeros(len(noise_eigvects[0]), dtype=np.complex_)

    f = float(k)/len(noise_eigvects[0])

    for i in range(0, len(noise_eigvects[0])):
        freq_vector[i] = np.conjugate(complex(np.cos(2 * pi* i * f), np.sin(2 * pi * i *f))) # steering vector e definition
        #freq_vector[i] = np.conjugate(np.exp(1j*i*f))
'''

M = np.linspace(0, len(noise_eigvects[0]), len(noise_eigvects[0]))

freq_vector = np.conjugate(np.exp(1j*M*2*pi)) #M complex exponentials w/ frequences from exp(0) to exp(2pi(M-1))

'''
sum1 = 0
for u in range(0, len(noise_eigvects)):
    #sum1 += (abs(np.dot(np.asarray(freq_vector).transpose(), np.asarray(noise_eigvects[u]))))**2 # |e^H * vk|^2
    sum1 +=  (abs(np.fft.fft(noise_eigvects[:, u], 128)))**2
'''


Pmusic =0
for u in range(0, len(noise_eigvects)):
    # single eigenvector sum
    sum2 = 0
    for k in range(0, len(noise_eigvects[0])):
        sum2 += np.dot(noise_eigvects[u, k] , freq_vector)
    sum3 = abs(sum2)**2
    Pmusic = np.append(Pmusic, 1/sum3)


plt.figure()
plt.plot(Pmusic[:int(len(Pmusic)/2)])
#plt.title("Estimation via MUSIC")
plt.show()
