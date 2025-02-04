import numpy as np
import matplotlib.pyplot as plt

def raised_cos(alpha, T):
    pi = np.pi
    cos = np.cos
    def sinc(x):
        return 1 if x==0 else np.sin(pi*x)/(pi*x)
    
    ht = np.zeros(64*2)
    for t in range(-64, 64):
        if (t == abs(T/2*alpha)):
            ht[t] = (pi/(4*T))*sinc(1/(2*alpha))
        else :
            ht[t] = (1/T)*sinc(t/T)*((cos(pi*alpha*t/T))/(1- (2*alpha*t/T)**2))
    return ht         

if __name__ == "__main__":
    h = raised_cos(0.2, 2)
    plt.plot(h)
    plt.show()