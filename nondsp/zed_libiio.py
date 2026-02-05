import adi
import numpy as np
import matplotlib.pyplot as plt
from fmfun import *

tx_buf_sz = 2**10
# Create device from specific uri address
sdr = adi.adrv9009(uri="ip:10.16.1.156")
sdr.calibrate
sdr.trx_lo = int(400e6)
sdr.rx_buffer_size = 2**15
sdr.tx_enabled_channels[0]
sdr.rx_enabled_channels[0]
sdr.tx_cyclic_buffer = True
sdr.rx_powerdown_en_chan1 = True
print("Local oscillator value in Mhz", sdr.trx_lo/1e6)

N = int(tx_buf_sz)
t = np.linspace(0, 2*np.pi, N)
a = 0.2

tri_shape1 = triagshape(t, a, 0, 0) #is shape
s1 = FMMOD(tri_shape1, N) #is fm fodulated
plt.plot(s1)
plt.show()

tx_data = 512*s1

sdr.tx([tx_data , np.zeros(tx_buf_sz)])

np.zeros(1024, dtype=np.float32)

data = sdr.rx()
plt.plot(np.real(data[0]) + np.imag(data[0]))
plt.show()
