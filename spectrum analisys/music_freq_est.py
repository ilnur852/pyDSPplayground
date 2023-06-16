import numpy as np
import matplotlib.pyplot as plt
from scipy import linalg as la

#parameters
N = 1024
p = 2
Nfft = 128
#vars 
pi = np.pi
f1 = 3
f2 = 24

def music_ps_direct(noise_eigvects, N):
    #perform MUSIC frequency estimation
    music_pseudospectrum =[]
    M = len(noise_eigvects[0])
    for f in range(N): # calculate for M number of frequencies 
        freq_vector = np.exp(1j*2*np.pi*f*np.linspace(0, M-1, num=len(noise_eigvects))/M) #M complex exponentials w/ frequences from exp(0) to exp(2*pi*f*(M-1))
        Pmu_w = 0
        for u in range(len(noise_eigvects)):
            # calculate power for sigle frequency
            Pmu_w += (abs(np.dot(np.conj(freq_vector), noise_eigvects[:, u])))**2 
        music_pseudospectrum = np.append(music_pseudospectrum, Pmu_w) #construct pseudospectrum via appending values
    return 1/music_pseudospectrum

def music_ps_fft(noise_eigvects, N):
    sum1 = 0
    for u in range(0, len(noise_eigvects)):
        sum1 += (abs(np.fft.fft(noise_eigvects[:, u], N)))**2
    return 1/(sum1[:len(sum1)//2])

#generate sequence
t = np.linspace(0, 2*pi, num=N)
x =  - 0.5*np.random.random(N) + np.sin(f1*t)# + np.cos(f2*t) 
plt.plot(x)
plt.show()

fft_x = abs(np.fft.fft(x, Nfft))
fft_x = fft_x[:len(fft_x)//2]
plt.plot(fft_x)
plt.title("Estimation via DFT")

#find autocorrelations
conj = np.conj(x)
flip = conj[::-1] 
acf =  np.convolve(x, flip) #autocorrelation function - convotution of time reversal of self
#construct autocorrelation matrix (Toeplitz)
Rxx = la.toeplitz(acf)
#eigendecomposition of Rxx
v, d = np.linalg.eig(Rxx) # v- eigenvalues , d - corresponding eigenvectors 
indexes = np.argsort(v)[::-1]
sort_eigvals = v[indexes] # sorting eigenvalues from greatest to least (retr)
sort_eigvects = d[:, indexes]
#separating signal and noise subspace eigenvectors
s_evects = sort_eigvects[0:p]
n_evects = sort_eigvects[p:len(sort_eigvects)]
print("length noise eigenvector", len(n_evects))

Pmusic= music_ps_direct(n_evects, Nfft)
Pmusic_fft = music_ps_fft(n_evects ,Nfft)

print(f1, f2)
print("max's of fft", (np.argsort(fft_x)[::-1][:p//2])*N/Nfft)
#print("max's of MUSIC (fft)", (np.argsort(Pmusic_fft)[::-1][:p//2])*N/Nfft)
print("max's of MUSIC (direct)", (np.argsort(Pmusic)[::-1][:p//2])/2)

plt.figure()
plt.plot(Pmusic)
plt.title("Estimation via MUSIC (direct)")
'''
plt.figure()
plt.plot(Pmusic_fft)
plt.title("Estimation via MUSIC (fft)")
'''
plt.show()
