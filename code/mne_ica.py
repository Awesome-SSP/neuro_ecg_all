import os
import mne
from mne.preprocessing import ICA, create_eog_epochs
import matplotlib.pyplot as plt

# ------------------------------------------------------------------
# Step 1: Load the EEG Data
# ------------------------------------------------------------------
# Specify the path to your EEGLAB .set file. We use a raw string (r'...') to avoid issues with backslashes.
set_file_path = 's17_1.set'
# Load the EEG data with preload=True to load all data into memory for faster processing.
raw = mne.io.read_raw_eeglab(set_file_path, preload=True)
print("Raw Data Loaded:")
print(raw)

# Plot the raw data to inspect the time-domain signal before ICA.
# Here we display 64 channels to see all available channels.
raw.plot(n_channels=64, title='Raw Data: Before ICA', show=True)

# ------------------------------------------------------------------
# Step 2: Preprocess the Data
# ------------------------------------------------------------------
# (Optional) Set a standard montage to define sensor locations. 
# 'standard_1020' is used because it is a common EEG montage.
montage = mne.channels.make_standard_montage('standard_1020')
raw.set_montage(montage, on_missing='warn')
# This step is crucial for ICA if sensor positions are used for component visualization.
print("Montage set to standard_1020.")

# Apply a band-pass filter to remove very slow drifts (<1 Hz) and high-frequency noise (>40 Hz).
# 1-40 Hz is a typical range for EEG analysis, preserving most neural signals.
raw.filter(l_freq=1, h_freq=40, fir_design='firwin')
# Now the data is cleaner and more suitable for ICA.
print("Band-pass filtering applied (1-40 Hz).")

# ------------------------------------------------------------------
# Step 3: Fit ICA to the Preprocessed Data
# ------------------------------------------------------------------
# Initialize the ICA object:
# - n_components=20: Choose to decompose the data into 20 independent components.
#   (This is often set based on the number of channels or by a desired dimensionality reduction.)
# - random_state=97: Sets a seed for reproducibility.
# - max_iter='auto': Let MNE decide the maximum iterations needed for convergence.
ica = ICA(n_components=20, random_state=97, max_iter='auto')
ica.fit(raw)  # Fit the ICA model on the filtered data.
print("ICA fitted on raw data.")

# ------------------------------------------------------------------
# Step 4: Inspect ICA Components
# ------------------------------------------------------------------
# Plot the ICA components' topographies.
# This visualization helps in identifying components that likely correspond to artifacts.
ica.plot_components(inst=raw)
# Optionally, you can inspect component properties (e.g., time series) to help decide which to exclude.
# e.g., ica.plot_properties(raw, picks=[0, 3])  # if you suspect components 0 and 3 are artifacts

# ------------------------------------------------------------------
# Step 5: Mark Artifact Components
# ------------------------------------------------------------------
# Based on visual inspection, suppose we identify components 0 and 3 as artifacts (e.g., eye blinks).
# These components will be excluded from the data during reconstruction.
ica.exclude = [0, 3]
print("Marked artifact components (to exclude):", ica.exclude)

# ------------------------------------------------------------------
# Step 6: Apply ICA to Remove Artifacts and Reconstruct Clean Data
# ------------------------------------------------------------------
# Create a copy of the raw data to apply ICA.
raw_clean = raw.copy()
# Apply the ICA solution, which removes the marked artifact components.
ica.apply(raw_clean)
print("ICA applied; artifact components removed.")

# ------------------------------------------------------------------
# Step 7: Visualize the Cleaned Data
# ------------------------------------------------------------------
# Plot the cleaned data to compare with the original data.
raw_clean.plot(n_channels=64, title="Cleaned Data after ICA", show=True)

# Optional: Use input() to keep the script running (especially in some environments)
input("Press Enter to exit...")