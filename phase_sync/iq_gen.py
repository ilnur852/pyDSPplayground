from math import copysign
import numpy as np
import matplotlib.pyplot as plt
from scipy import signal
from carr_sync import carrier_sync

def downsample(input_arr, N, factor):
    k = 0
    M = int(N / factor)
    output_arr = np.zeros(M)
    for k in range(M):
        output_arr[k] = input_arr[int(k * factor + factor / 2)]
    return output_arr

'''Configuration sequence'''
save_file = False
'''----------------------'''
outfile1 = open("outQ.txt", "w")
outfile2 = open("outI.txt", "w")

# Global constants
num_symbols = 200
N = 500000

# Crate random samples
x_int = np.random.randint(0, 8, num_symbols)  # 0 to 3

x_degrees = x_int * 360 / 8.0 + 45  # //calculate phase shift degrees for each symbol
x_radians = x_degrees * np.pi / 180.0  # sin() and cos() takes in radians
x_symbols = np.cos(x_radians) + 1j * np.sin(x_radians)  # this produces our PSK complex symbols

plt.plot(np.real(x_symbols), np.imag(x_symbols), '.')
plt.show()
# Create sine and cosine waves
x = np.linspace(0, N / 4, N)

coder_sw = np.sin(x)
coder_cw = np.cos(x)

symbols = np.zeros(0)

# repeat symbols for N/num_symbols
i = 0
for i in range(num_symbols):
    symbols = np.append(symbols, np.ones(int(N / num_symbols)) * x_symbols[i]) 
# Apply mixing
out_sym = (coder_sw * np.real(symbols) + coder_cw * np.imag(symbols))

# decoder side sine and cosine
freq_shift = 1
x = np.linspace(0, (N / 4 + freq_shift), N)
decoder_sw = np.sin(x)
decoder_cw = np.cos(x)

# Apply rx mixer to 0 freq
decoded_Q = out_sym * decoder_sw
decoded_I = out_sym * decoder_cw

# filtering using fir
taps = 25
f = 0.01
fir = signal.firwin(taps, f)
lQ = signal.filtfilt(fir, 1.0, decoded_Q)
lI = signal.filtfilt(fir, 1.0, decoded_I)

si = np.zeros(N)
sq = np.zeros(N)

# dowmsample
dsQ = downsample(lQ, N, 50) 
dsI = downsample(lI, N, 50) 
#dsQ = lQ
#dsI = lI
# Save if necessary
if save_file:
    for i in range(len(dsQ)):
        fQ = (np.floor(dsQ[i])).astype(int)
        fI = (np.floor(dsI[i])).astype(int)
        'print (sig[i] , fl)'
        outfile1.write(np.binary_repr(fQ, width=12) + "\n")
        outfile2.write(np.binary_repr(fI, width=12) + "\n")

# round if necessary
dsQ = np.round(dsQ, 3)
dsI = np.round(dsI, 3)

# create complex array
complex_sig = dsQ + 1j * dsI

# Create new carrier sync class instance
cs = carrier_sync()
# Apply carrier sync
NbW = .25 # normalized bandwidth
damp_fctr = .707  # dampling factor
sympsamp = 100  # samples per symbol
Ki, Kp = cs.calcloopgains(NbW, damp_fctr, sympsamp)
sout, phase, ev = cs.stepImpl(complex_sig, Ki=Ki, Kp=Kp)
sout_cordic, phase_cordic, ev_cordic = cs.stepImplcordic(complex_sig, Ki=Ki, Kp=Kp)

print("Ki is", Ki, "\n Kp is", Kp)
# Plot routine

plt.plot(np.real(complex_sig), np.imag(complex_sig), '.')
plt.title('RX symbols') 
plt.grid(True) 
plt.show()

plt.plot(np.real(sout[3000:5000]), np.imag(sout[3000:5000]), '.')
plt.title('Phase/carrier estimated using DDS')
plt.grid(True)
plt.show()

plt.plot(np.real(sout_cordic[3000:5000]), np.imag(sout_cordic[3000:5000]), '.')
plt.title('Input rotated via CoRDiC')
plt.grid(True)
plt.show()

plt.plot(ev)
plt.title('Phase error in DDS')
plt.show()

plt.plot(ev_cordic)
plt.title('Phase error in CoRDiC')
plt.show()

plt.subplot(611)
plt.plot(np.real(complex_sig))
plt.grid(True)
plt.subplot(612)
plt.plot(np.imag(complex_sig))
plt.grid(True)
plt.subplot(613)
plt.plot(sout)
plt.grid(True)
plt.subplot(614)
plt.plot(sout)
plt.grid(True)
plt.subplot(615)
plt.plot(np.imag(sout_cordic))
plt.grid(True)
plt.subplot(616)
plt.plot(np.real(sout_cordic))
plt.grid(True)
plt.show()
