import matplotlib.pyplot as plt
import numpy as np
from scipy.signal import butter, lfilter, cheby1

import librosa

def load_signal(filepath: str,): 
    y, fs = librosa.load(filepath, sr=None) 
    y = librosa.to_mono(y)
    order = 3
    low = 120.0
    high= 900.0
    b,a = butter(order, [low, high], fs=fs, btype='band')
    y[np.abs(y) < 0.03] = 0
    filtered_sound = lfilter(b, a ,y)
    y = filtered_sound

    return y, fs

def plot_signal(y, fs):
    t = np.linspace(0, len(y)/fs, 1/fs)
    plt.plot(t, y)
    plt.xlabel("Time (s)")
    plt.ylabel("Amplitude")
    plt.show()
    

def plot_fft(y, fs): 
    fft_frequencies = np.fft.rfftfreq(len(y), 1/fs)
    sound_fft = np.fft.rfft(y) 
    plt.plot(np.where((fft_frequencies > 100) & (fft_frequencies < 1300), fft_frequencies, None) , np.abs(sound_fft))
    plt.xlabel("Frequency (Hz)")
    plt.ylabel("Amplitude")


def find_fundamental_frequency(fft, fft_frequencies):
    thrershold = 190
    notes = []
    for j in range(len(fft)):
        amplitude = np.abs(fft[j])
        freq = round(fft_frequencies[j], 2)
        if freq > 1000 or freq < 80:
            continue
        if amplitude > thrershold: 
            notes.append([freq, round(amplitude,2)])

    if notes == []:
        return None
    # for n in notes:
        # print(librosa.hz_to_note(n[0]), n[1], end=" || ")
    return min(notes, key = lambda x: x[0])

def find_notes(y, fs): 
    onset_frames = librosa.onset.onset_detect(y=y)
    onset_samples = librosa.frames_to_samples(onset_frames)

    notes = []

    for i in range(0, len(onset_samples) -1):
        window = y[onset_samples[i]: onset_samples[i+1]]
        fft_frequencies = np.fft.rfftfreq(len(window), 1/fs)
        fft = np.fft.rfft(window)
        notes_from_sequence = find_fundamental_frequency(fft, fft_frequencies)
        if notes_from_sequence != None:
            notes.append(librosa.hz_to_note(notes_from_sequence[0]))


    final_window = y[onset_samples[-1]:]
    fft_frequencies = np.fft.rfftfreq(len(final_window), 1/fs)
    fft = np.fft.rfft(final_window)
    notes_from_sequence = find_fundamental_frequency(fft, fft_frequencies)
    if notes_from_sequence != None:
        notes.append(librosa.hz_to_note(notes_from_sequence[0]))
    return notes

