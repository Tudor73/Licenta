import numpy as np
import math
import time
import matplotlib.pyplot as plt
from datetime import datetime, date


def DFT(x): 
    N = len(x)
    X = [0 for i in range(N)]
    for k in range(N):
        for i in range(N): 
            X[k] = X[k] + x[i] * math.e**(-2j * math.pi * k * i / N)

    return X

def FFT(x):
    N = len(x)
    if N < 32: 
        return DFT(x)
    X_par = FFT(x[0:N:2])
    X_impar = FFT(x[1: N:2])
    X = [0 for i in range(N)]
    
    for k in range(N//2):
        e = math.e**(-2j * math.pi * k  / N)
        X[k] = X_par[k] + e * X_impar[k]
        X[k + N//2] = X_par[k] - e * X_impar[k]
    return X 

x = np.random.random(32)  





inputs = []
input_size = 32
dft_times = []
fft_times = []
numpy_times = []


for i in range(9):
    x = np.random.random(input_size)
    start_time = datetime.now()
    y = DFT(x)
    end_time = datetime.now()
    duration = end_time - start_time
    dft_times.append(duration.total_seconds())

    start_time = datetime.now()
    y = FFT(x)
    end_time = datetime.now()
    duration = end_time - start_time
    fft_times.append(duration.total_seconds())

    start_time = datetime.now()
    y = np.fft.fft(x)
    end_time = datetime.now()
    duration = end_time - start_time
    numpy_times.append(duration.total_seconds())

    inputs.append(input_size)
    input_size *= 2
    

plt.figure(figsize=(8,5))
plt.plot(inputs, dft_times, label='DFT')
plt.plot(inputs, fft_times, label='FFT')
plt.plot(inputs, numpy_times, label='Numpy FFT')
plt.xlabel('Input size')
plt.ylabel('Time (s)')
plt.legend(loc="upper left")
plt.savefig('fft.png')
plt.show()

