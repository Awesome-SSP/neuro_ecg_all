# %%
import os
import mne

# %%
# ------------------------------------------------------------------
# Step 1: Load custom Data
# ------------------------------------------------------------------
# sample_data_folder = mne.datasets.sample.data_path()
set_file_path = 's17_1.set'
raw = mne.io.read_raw_eeglab(set_file_path, preload=True)

# %%
# Plot raw data to inspect before filtering
print("Raw Data")
print(raw)
raw.plot(n_channels=10, title='Raw Data: Before Filtering')

# %%
# ------------------------------------------------------------------
# Step 2: Band-Pass Filtering (e.g., 1 to 40 Hz)
# ------------------------------------------------------------------
print("Band-Pass Filtering (1-40 Hz)")
raw_bandpass = raw.copy().filter(l_freq=1, h_freq=40, fir_design='firwin')
raw_bandpass.plot(n_channels=10, title='After Band-Pass Filter (1-40 Hz)')

# %%
# ------------------------------------------------------------------
# Step 3: High-Pass Filtering (e.g., removing drifts below 1 Hz)
# ------------------------------------------------------------------
print("High-Pass Filtering (Cutoff = 1 Hz)")
raw_highpass = raw.copy().filter(l_freq=1, h_freq=None, fir_design='firwin')
raw_highpass.plot(n_channels=10, title='After High-Pass Filter (Cutoff = 1 Hz)')

# %%
# ------------------------------------------------------------------
# Step 4: Low-Pass Filtering (e.g., removing frequencies above 40 Hz)
# ------------------------------------------------------------------
print("Low-Pass Filtering (Cutoff = 40 Hz)")
raw_lowpass = raw.copy().filter(l_freq=None, h_freq=40, fir_design='firwin')
raw_lowpass.plot(n_channels=10, title='After Low-Pass Filter (Cutoff = 40 Hz)')

# %%
# ------------------------------------------------------------------
# Step 5: Notch Filtering (e.g., removing 50 Hz line noise)
# ------------------------------------------------------------------
print("Notch Filtering (49 & 51 Hz)")
raw_notch = raw.copy().notch_filter(freqs=[49, 51], fir_design='firwin')
raw_notch.plot(n_channels=10, title='After Notch Filter (49 & 51 Hz)')

# %%
# ------------------------------------------------------------------
# Optional: Compare Frequency Spectrum Before and After Filtering
# ------------------------------------------------------------------
def plot_power_spectrum(data, title):
    # Compute the power spectral density (PSD)
    psd = data.compute_psd(fmax=100, average='mean')
    # Plot the computed PSD and get the figure handle
    fig = psd.plot()  # no title parameter allowed here
    # Set the title on the figure
    fig.suptitle(title)
    # Optionally, force a redraw of the canvas
    fig.canvas.draw()
print('Original Data Spectrum=========================================================================================================')
plot_power_spectrum(raw, 'Original Data Spectrum')
print('Band-Pass Filtered Spectrum=========================================================================================================')
plot_power_spectrum(raw_bandpass, 'Band-Pass Filtered Spectrum (1-40 Hz)')
print('Notch Filtered Spectrum=========================================================================================================')
plot_power_spectrum(raw_notch, 'Notch Filtered Spectrum (49 & 51 Hz)')

# %%
# Optional: Use input() to keep the script running (especially in some environments)
input("Press Enter to exit...")