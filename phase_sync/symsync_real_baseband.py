import numpy as np
import matplotlib.pyplot as plt
from symbol_sync import symsync_lgc
from carr_sync import carrsync_dds_lgc as cs

pi = np.pi
f = np.fromfile(open("baseband_out"), dtype=np.complex64)


bsbnd =  f[:200000]
print(len(bsbnd))

#symbol syncronize using symsync
ssamp, ev = symsync_lgc(bsbnd, 130, 16, 64) 

plt.scatter(np.imag(ssamp[200:]), np.real(ssamp[200:]), s=8)
plt.show()

print(len(ssamp))
#carrier phase syncronize using carrsync
csync, pherr, errv_cs = cs(ssamp, 0.1, 1, 1)

plt.scatter(np.real(csync), np.imag(csync), s=3)
plt.show()

'''
x_int = np.arange(0,8,1) # 0 to 3
x_degrees = x_int * 360//8 + 45/2  # //calculate phase shift degrees for each symbol
x_radians = x_degrees * np.pi / 180.0  # sin() and cos() takes in radians
x_symbols = np.cos(x_radians) + 1j * np.sin(x_radians)  # this produces our PSK complex symbols

def ed2d(x, y):
    return np.max([(abs((np.real(x) - np.real(y)))) , (abs((np.imag(x) - np.imag(y))))])

def min_ed(arr, x): #find euclidian distance between input array(arr) and value x
    dests = []
    for i in range(len(arr)):
        dests = np.append(dests, ed2d(arr[i], x))
    return np.min(dests), np.argmin(dests)
'''
