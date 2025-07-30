import os
import mne
import numpy as np
import matplotlib.pyplot as plt
from mne.time_frequency import psd_array_welch

# ------------------------------------------------------------------
# Step 1: Load EEG Data from an EEGLAB file
# ------------------------------------------------------------------
# Use a raw string literal for the file path to avoid escape errors
set_file_path = 's17_1.set'
raw = mne.io.read_raw_eeglab(set_file_path, preload=True)
print("Raw Data:")
print(raw)
# Optional: Plot raw data for time-domain inspection
raw.plot(n_channels=10, title='Raw Data: Before Filtering')

# ------------------------------------------------------------------
# Step 2: Apply Bandpass Filter (1-40 Hz)
# ------------------------------------------------------------------
print("Applying Bandpass Filter (1-40 Hz)")
raw_bandpass = raw.copy().filter(l_freq=1, h_freq=40, fir_design='firwin')
raw_bandpass.plot(n_channels=10, title='After Bandpass Filter (1-40 Hz)')

# ------------------------------------------------------------------
# Step 3: Compute PSDs Before and After Filtering
# ------------------------------------------------------------------
def compute_average_psd(raw_data, fmax=60):
    """
    Compute the power spectral density (PSD) of a Raw object and
    return the frequency axis and the average PSD across channels.
    """
    data = raw_data.get_data()  # shape: (n_channels, n_times)
    sfreq = raw_data.info['sfreq']
    # Compute PSD using Welch's method
    psds, freqs = psd_array_welch(data, sfreq=sfreq, fmin=0, fmax=fmax, n_fft=2048)
    # Average PSD across channels for a single representative curve
    mean_psd = np.mean(psds, axis=0)
    return freqs, mean_psd

# Compute PSD for original raw data
freqs_raw, mean_psd_raw = compute_average_psd(raw, fmax=60)
# Compute PSD for bandpass filtered data
freqs_bp, mean_psd_bp = compute_average_psd(raw_bandpass, fmax=60)

# ------------------------------------------------------------------
# Step 4: Plot PSD Comparison
# ------------------------------------------------------------------
plt.figure(figsize=(8, 6))
plt.plot(freqs_raw, mean_psd_raw, label='Original Raw')
plt.plot(freqs_bp, mean_psd_bp, label='Bandpass Filtered (1-40 Hz)')
plt.xlabel('Frequency (Hz)')
plt.ylabel('Power Spectral Density')
plt.title('PSD Comparison: Before and After Bandpass Filtering')
plt.legend()
plt.tight_layout()
plt.show()


# Optional: Use input() to keep the script running (especially in some environments)
input("Press Enter to exit...")


"""
Explanation

Load EEG Data:

    The EEG data is loaded from your EEGLAB file using mne.io.read_raw_eeglab() with preload=True (this loads all the data into memory).

    A quick plot of the raw data is generated to inspect the time-domain signals.

Apply Bandpass Filter:

    A bandpass filter between 1 and 40 Hz is applied to the raw data using raw.copy().filter().

    This filter removes very low frequencies (drifts) and high frequencies (noise) that are outside the range of interest.

Compute PSD:

    The function compute_average_psd() calculates the power spectral density (PSD) using Welch's method via psd_array_welch().

    It returns the frequency values and the average PSD across all channels, giving a representative spectrum of the entire dataset.

Plot PSD Comparison:

    The PSD for the original raw data and the bandpass filtered data are plotted together on the same figure.

    This comparison allows you to see how the filter affects the frequency content: you should observe that frequencies outside the 1–40 Hz range are attenuated in the filtered data.

"""