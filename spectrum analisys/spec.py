import numpy as np
import matplotlib.pyplot as  plt
from scipy.signal import periodogram

x = 10*np.sin(np.linspace(0, 40*np.pi, 2000)) + 3*np.sin(np.linspace(0, 200*np.pi, 2000)) + 0.5*np.sin(np.linspace(0, 600*np.pi, 2000)) 

plt.plot(x)
plt.show()

h, Pxx = periodogram(x, 512, 'flattop', scaling='spectrum')
plt.semilogy(h, Pxx)
#plt.ylim([1e-4, 1e0])
plt.show()
