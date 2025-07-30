import os
import mne
import numpy as np
import matplotlib.pyplot as plt
from mne.time_frequency import psd_array_welch

# ------------------------------------------------------------------
# Step 1: Load the EEG Data (EEGLAB .set file)
# ------------------------------------------------------------------
set_file_path = 's17_1.set'
raw = mne.io.read_raw_eeglab(set_file_path, preload=True)
print("Raw Data Loaded:")
print(raw)

# Optional: Plot the time-domain data for inspection
raw.plot(n_channels=64, title='Raw Data: Before Filtering', show=True)

# ------------------------------------------------------------------
# Step 2: Plot the Frequency-Domain Data using compute_psd()
# ------------------------------------------------------------------
# Compute the PSD up to 100 Hz using the new compute_psd() API.
psd_obj = raw.compute_psd(fmax=100, average='mean')
# Extract the PSD and frequency values from the Spectrum object.
psds, freqs = psd_obj.get_data(return_freqs=True)

# Plot the PSD using the built-in plot method.
fig = psd_obj.plot(show=True)
# Set a title on the returned figure.
fig.suptitle("Raw Data: Frequency Domain (PSD)")
fig.canvas.draw()
plt.show()

# ------------------------------------------------------------------
# Step 3: Alternative: Manually Compute and Plot Average PSD using psd_array_welch
# ------------------------------------------------------------------
def compute_and_plot_psd(raw_data, fmax=100, label="PSD"):
    # Get the raw data and sampling frequency
    data = raw_data.get_data()  # shape: (n_channels, n_times)
    sfreq = raw_data.info['sfreq']
    # Compute PSD using Welch's method
    from mne.time_frequency import psd_array_welch
    psds, freqs = psd_array_welch(data, sfreq=sfreq, fmin=0, fmax=fmax, n_fft=2048)
    # Average PSD across channels for a single representative curve
    mean_psd = np.mean(psds, axis=0)
    return freqs, mean_psd

# Compute PSD for original raw data
freqs_raw, mean_psd_raw = compute_and_plot_psd(raw, fmax=100)

# Plot the manually computed average PSD
plt.figure(figsize=(8, 6))
plt.plot(freqs_raw, mean_psd_raw, label="Original Raw")
plt.xlabel("Frequency (Hz)")
plt.ylabel("Power Spectral Density")
plt.title("Average PSD Across Channels (Original Data)")
plt.legend()
plt.tight_layout()
plt.show()


# Optional: Use input() to keep the script running (especially in some environments)
input("Press Enter to exit...")