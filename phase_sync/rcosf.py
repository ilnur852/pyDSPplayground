import numpy as np
import matplotlib.pyplot as plt
from numpy.core.numeric import roll
from scipy import signal

def raised_root_cosine(upsample, num_positive_lobes, alpha):
    """
    Root raised cosine (RRC) filter (FIR) impulse response.

    upsample: number of samples per symbol

    num_positive_lobes: number of positive overlaping symbols
    length of filter is 2 * num_positive_lobes + 1 samples

    alpha: roll-off factor
    """

    N = upsample * (num_positive_lobes * 2 + 1)
    t = (np.arange(N) - N / 2) / upsample

    # result vector
    h_rrc = np.zeros(t.size, dtype=np.float)

    # index for special cases
    sample_i = np.zeros(t.size, dtype=np.bool)

    # deal with special cases
    subi = t == 0
    sample_i = np.bitwise_or(sample_i, subi)
    h_rrc[subi] = 1.0 - alpha + (4 * alpha / np.pi)

    subi = np.abs(t) == 1 / (4 * alpha)
    sample_i = np.bitwise_or(sample_i, subi)
    h_rrc[subi] = (alpha / np.sqrt(2)) \
                * (((1 + 2 / np.pi) * (np.sin(np.pi / (4 * alpha))))
                + ((1 - 2 / np.pi) * (np.cos(np.pi / (4 * alpha)))))

    # base case
    sample_i = np.bitwise_not(sample_i)
    ti = t[sample_i]
    h_rrc[sample_i] = np.sin(np.pi * ti * (1 - alpha)) \
                    + 4 * alpha * ti * np.cos(np.pi * ti * (1 + alpha))
    h_rrc[sample_i] /= (np.pi * ti * (1 - (4 * alpha * ti) ** 2))

    return h_rrc

if __name__ == "__main__":
    # Global constants
    save_file = False
    outfile1 = open("outQ.txt", "w")
    outfile2 = open("outI.txt", "w")

    num_symbols = 300
    N = 100*num_symbols

    # Crate random samples
    x_int = np.random.randint(0, 8, num_symbols)  # 0 to 
    #x_int = np.array([3,6,8,1,4,5,4,7,1,2,3,0,2,6,3,2,7,1,3,4])
    print(len(x_int))
    x_degrees = x_int * 360 / 8.0 + 35  # //calculate phase shift degrees for each symbol
    x_radians = x_degrees * np.pi / 180.0  # sin() and cos() takes in radians
    x_symbols = np.cos(x_radians) + 1j * np.sin(x_radians)  # this produces our PSK complex symbols

    i = 0
    symbols = np.zeros(0)
    for i in range(num_symbols):
        symbols = np.append(symbols, np.ones(int(N / num_symbols)) * x_symbols[i])

    h = raised_root_cosine(int(N / num_symbols), 1, 0.6)

    filts = np.convolve(h, symbols)
    dsQ = np.real(filts)*5
    dsI = np.imag(filts)*5


    if save_file:
        for i in range(len(dsQ)):
            fQ = (np.floor(dsQ[i])).astype(int)
            fI = (np.floor(dsI[i])).astype(int)
            'print (sig[i] , fl)'
            outfile1.write(np.binary_repr(fQ, width=12) + "\n")
            outfile2.write(np.binary_repr(fI, width=12) + "\n")

    print(len(dsQ))

    print('ff')
    plt.plot(dsQ)
    plt.plot(dsI)
    plt.show()

