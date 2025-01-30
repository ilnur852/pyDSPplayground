import numpy as np
import matplotlib.pyplot as plt
from scipy import linalg as la

#parameters
N = 512
p = 4
Nfft = 4096
#vars 
pi = np.pi
f1 = 50.23
f2 = 14.4

def music_ps_direct(noise_eigvects, N):
    #perform MUSIC frequency estimation
    music_pseudospectrum =[]
    M = len(noise_eigvects[0])
    for f in range(N): # calculate for N number of frequencies 
        freq_vector = np.exp(1j*2*np.pi*f*np.linspace(0, M-1, num=len(noise_eigvects))/M) #M complex exponentials w/ frequences from exp(0) to exp(2*pi*f*(M-1))
        Pmu_w = 0.0
        for u in range(len(noise_eigvects[1])):
            # calculate power for sigle frequency
            Pmu_w += (abs(np.dot(np.conj(freq_vector), noise_eigvects[:, u])))**2 
        music_pseudospectrum = np.append(music_pseudospectrum, Pmu_w) #construct pseudospectrum via appending values
    return 1.0/music_pseudospectrum

def music_ps_fft(noise_eigvects, N):
    sum1 = 0
    for u in range(0, len(noise_eigvects[1])):
        sum1 += (abs(np.fft.fft(noise_eigvects[:, u], N)))**2
    return 1/(sum1[:len(sum1)//2])

if __name__=="__main__":
    #generate sequence
    t = np.linspace(0, 2*pi, num=N)
    x =  0.5*np.random.random(N) + np.sin(f1*t) + 0.6*np.cos(f2*t) 
    plt.plot(x)
    plt.show()

    fft_x = abs(np.fft.fft(x, Nfft))
    fft_x = fft_x[:len(fft_x)//2]
    plt.plot(fft_x)
    plt.title("Estimation via DFT")

    #find autocorrelations
    conj = np.conj(x)
    flip = conj[::-1] 
    acf =  np.convolve(x, flip) #autocorrelation sequence - convotution of time reversal of self
    #construct autocorrelation matrix (Toeplitz)
    Rxx = la.toeplitz(acf)
    #eigendecomposition of Rxx
    v, d = np.linalg.eig(Rxx) # v- eigenvalues , d - corresponding eigenvectors (column vectors - see docs)
    indexes = np.argsort(v)[::-1]
    sort_eigvals = v[indexes] # sorting eigenvalues from greatest to least (retr)
    sort_eigvects = d[:, indexes]
    #separating signal and noise subspace eigenvectors
    s_evects = sort_eigvects[0:p]
    n_evects = sort_eigvects[:, p:len(sort_eigvects)]
    print("length of noise eigenvector", len(n_evects))

    Pmusic= music_ps_direct(n_evects, Nfft)
    #Pmusic_fft = music_ps_fft(n_evects ,Nfft)

    print("frequencies of stimulus", f1, f2)
    print("max's of fft", (np.argsort(fft_x)[::-1][:p//2])*N/Nfft)
    #print("max's of MUSIC (fft)", (np.argsort(Pmusic_fft)[::-1][:p//2])*N/Nfft)
    print("max's of MUSIC (direct)", (np.argsort(Pmusic)[::-1][:p//2])/2)

    
    plt.figure()
    plt.plot(Pmusic)
    plt.title("Estimation via MUSIC (direct)")
    
    #plt.figure()
    #plt.plot(Pmusic_fft)
    #plt.title("Estimation via MUSIC (fft)")

    plt.show()
