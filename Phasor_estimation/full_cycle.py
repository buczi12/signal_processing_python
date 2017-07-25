# This script aim is to present phasor estimation algorithm used in power system protection
# estimation is based on DFT calculated only for base frequency (50Hz in power system)
# the estimation result is RMS value and phase of sinusoidal signal in time
from math import pi as pi
import numpy as np
import matplotlib.pyplot as plt
from scipy import signal

# functions definitions


def full_cycle(source, f_s, fn):
    freqs = [i + 1 for i in range(int(f_s/fn))]
    # real part coeffs
    re = [(np.exp(freq * 2j * pi / (f_s/fn)) * np.sqrt(2) / (f_s/fn)).real for freq in freqs]
    # imag part coeffs
    im = [(np.exp(freq * 2j * pi / (f_s/fn)) * np.sqrt(2) / (f_s/fn)).imag for freq in freqs]

    # filtering - real and imag values estimation
    real = signal.lfilter(re, [1], source)
    imag = signal.lfilter(im, [1], source)

    # magnitude estimation
    mag = abs(real + imag*1j)
    # phase estimation
    pha = 2 * np.arctan(imag/real)

    return mag, pha


def half_cycle(source, f_s, fn):
    freqs = [2 * i for i in range(int(f_s/2/fn))]
    # real part coeffs
    re = [(2 * np.exp(freq * 1j * pi / (f_s/fn)) * np.sqrt(2) / (f_s/fn)).real for freq in freqs]
    # imag part coeffs
    im = [(2 * np.exp(freq * 1j * pi / (f_s/fn)) * np.sqrt(2) / (f_s/fn)).imag for freq in freqs]

    # filtering - real and imag values estimation
    real = signal.lfilter(re, [1], source)
    imag = signal.lfilter(im, [1], source)

    # magnitude estimation
    mag = abs(real + imag*1j)
    # phase estimation
    pha = 2 * np.arctan(imag/real)

    return mag, pha


# Test data generation
# Electrical system parameters
f1 = 50                                           # [Hz]
A = 110 * np.sqrt(2)                              # [kV]
# sampling frequency
fs = 2e3                                          # [Hz]
t = np.arange(0, 1.5/f1, 1/fs)                    # [s]
phi0 = 0                                          # [rad]
# signal generation
sig = A * np.sin(2 * pi * f1 * t + phi0)

# choose estimation method
magnitude1, phase1 = half_cycle(sig, fs, f1)
magnitude2, phase2 = full_cycle(sig, fs, f1)
# theoretical RMS value for visualization
rms = [A/np.sqrt(2) for k in range(len(t))]

# Signals plots
plt.figure(1)
plt.subplot(211)
plot1, = plt.plot(1e3 * t, sig, label="original signal")
plot3, = plt.plot(1e3 * t, magnitude1, 'g--', label="half-cycle")
plot4, = plt.plot(1e3 * t, magnitude2, 'm--', label="full-cycle")
plot2, = plt.plot(1e3 * t, rms, 'r', label="theoretical RMS value")
plt.legend(handles=[plot1, plot2, plot3, plot4], loc=4)
plt.title("RMS and phase estimation of 110kV sinusoid")
plt.ylabel("Voltage [kV]")
plt.xlabel("time [s]")
plt.grid()

plt.subplot(212)
plot1, = plt.plot(1e3 * t, phase1, 'g--', label="half-cycle")
plot2, = plt.plot(1e3 * t, phase2, 'm--', label="full-cycle")
plt.legend(handles=[plot1, plot2], loc=4)
plt.xlabel("time [s]")
plt.ylabel("Phase [rad]")
plt.grid()

plt.show()

