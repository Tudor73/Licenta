from pydub import AudioSegment
import matplotlib.pyplot as plt
import numpy as np
from scipy.signal import butter, lfilter, cheby1
import librosa


y = AudioSegment.from_wav("inputs/chitara_inreg2.wav")

filtered = y.high_pass_filter(120)


SEGMENT_MS = 50
# dBFS is decibels relative to the maximum possible loudness
volume = [segment.dBFS for segment in y[::SEGMENT_MS]]
volume2 = [segment.dBFS for segment in filtered[::SEGMENT_MS]]

x_axis = np.arange(len(volume)) * (SEGMENT_MS / 1000)
x_axis2 = np.arange(len(volume2)) * (SEGMENT_MS / 1000)

plt.plot(x_axis, volume)
plt.plot(x_axis2, volume2, color='red')

plt.show()

