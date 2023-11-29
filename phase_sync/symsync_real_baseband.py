import numpy as np
import matplotlib.pyplot as plt
from symbol_sync import symsync_lgc
from carr_sync import carrsync_cordic_lgc as cs

pi = np.pi
f = np.fromfile(open("baseband_out"), dtype=np.complex64)

bsbnd =  3*f[0:400000]
#symbol syncronize using symsync
ssamp, ev = symsync_lgc(bsbnd, 35, 0.707, 16)
#carrier phase syncronize using carrsync
csync, pherr, errv_cs = cs(ssamp, 0.05, 1, 1)

plt.scatter(np.real(csync[4000:]), np.imag(csync[4000:]), s=0.5)
plt.plot()

'''Just create 8PSK constellation template'''
x_int = np.arange(0,8,1) # 0 to 3
x_degrees = x_int * 360//8 + 45/2  # //calculate phase shift degrees for each symbol
x_radians = x_degrees * np.pi / 180.0  # sin() and cos() takes in radians
x_symbols = np.cos(x_radians) + 1j * np.sin(x_radians)  # this produces our PSK complex symbols

def ed2d(x, y):
    return np.sqrt((np.real(x)- np.real(y))**2 + (np.imag(x)- np.imag(y))**2)

def min_ed(arr, x): #find euclidian distance between input array(arr) and value x
    dests = []
    for i in range(len(arr)):
        dests = np.append(dests, ed2d(arr[i], x))
    return np.min(dests)

ek = []
for i in range(len(csync)):
    ek = np.append(ek, min_ed(x_symbols, csync[i]))
    #filter taps
    wi = np.ones(8)
    wq = np.ones(8)

plt.figure()
plt.plot(ek)
plt.show()
