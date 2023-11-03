import numpy as np
import matplotlib.pyplot as plt
from symbol_sync import symsync_lgc
from carr_sync import carrsync_cordic_lgc as cs

f = np.fromfile(open("baseband_out"), dtype=np.complex64)

bsbnd =  f[0:100000]
#symbol syncronize using symsync
ssamp, ev = symsync_lgc(bsbnd, 35, 0.707, 16)
#carrier phase syncronize using carrsync
csync, pherr, errv_cs = cs(ssamp, 0.05, 1, 1)

plt.plot(np.real(csync[4000:]), np.imag(csync[4000:]), '.')

plt.figure()
plt.plot(ev)
plt.plot(errv_cs)
plt.show()
