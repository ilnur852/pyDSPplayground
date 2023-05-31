from operator import le
import re
import numpy as np
import matplotlib.pyplot as plt

def cordic(x0, y0, theta, itnum):
    pi = np.pi

    while (theta > np.pi):
        theta = theta - pi*2

    if (theta > pi/2):
        theta = theta - pi
        x0 = x0
        y0 = y0 
        x, y = cordicrotate(x0, y0, theta, itnum)
    elif (theta < -pi/2):
        theta = theta + pi
        x0 = x0
        y0 = y0 
        x, y = cordicrotate(x0, y0, theta, itnum)
    else:
        theta = -theta
        x0 = x0
        y0 = -y0 
        x, y = cordicrotate(x0, y0, theta, itnum)
        x = -x
    
    return x, y
    
def cordicrotate(x0, y0, theta, itnum):
    p =np.arange(0,itnum,1) #numbers from 0 to itnum-1
    r = 1/np.power(2,p) # calc 2^-p
    #arctans = np.rad2deg(np.arctan(r))
    arctans = np.arctan(r)
    #input angle to rotate
    sigmak = np.zeros(itnum)
    xk = np.zeros(itnum+1)
    yk = np.zeros(itnum+1)
    zi = np.zeros(itnum+1)

    xk[0] = x0 #initial vector 
    yk[0] = y0
    zi[0] = theta
    i = 0
    pi = np.pi

    for i in range(itnum):
        sigmak[i] = np.sign(zi[i])
        xk[i+1] = xk[i] - sigmak[i]* yk[i] * r[i]
        yk[i+1] = yk[i] + sigmak[i]* xk[i] * r[i]
        zi[i+1] = zi[i] - sigmak[i]* arctans[i]

    x_res = -xk[itnum]*0.607
    y_res = yk[itnum]*0.607
    return(x_res, y_res)

if __name__ == "__main__":
    x0 = 10
    y0 = 0
    theta = 0
    angles = np.arange(-4*np.pi, 4*np.pi, step=0.1)
    i = 0 
    x = np.zeros(len(angles))
    y = np.zeros(len(angles))
    for i in range(len(angles)):
          x[i] , y[i] = cordic(x0, y0, angles[i], 32)
    
    plt.plot(angles, y)
    plt.plot(angles, x)
    plt.show()
