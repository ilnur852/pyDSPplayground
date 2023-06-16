import numpy as np
import matplotlib.pyplot as plt

N = 1000
M = 4

sin = np.sin
cos = np.cos

#Modulating signal, i.e M periods of sine
x = 0.8*sin(np.linspace(0, 2*M*np.pi, N))

w0_I = cos(np.linspace(0,N/4,N))
w0_Q = sin(np.linspace(0,N/4,N))

omega = N/M
deviation_freq = 10

#print(deviation_freq/omega)
integral_x = [0]
I = []
Q = []
i =0
for i in range(len(x)-1):
    integral_x = np.append(integral_x, np.sum(x[:i]))

I = cos(deviation_freq*integral_x)
Q = sin(deviation_freq*integral_x)

PM = I*w0_I + Q*w0_Q

plt.grid()
plt.plot(PM)
plt.show()
