import numpy as np
import matplotlib.pyplot as  plt

with open("From_ADC_2.txt", "r") as fl:
    x_data = fl.readlines()
fl.close()

x = []
for i in range(len(x_data)):
    x = np.append(x, int(x_data[i]))



plt.plot(x)
plt.show()
