import os
import mne
import matplotlib.pyplot as plt

# -----------------------------
# Step 1: Load Data and Show Before Marking Bad Channels
# -----------------------------
# Use a raw string for the file path to avoid escape issues.
set_file_path = 's17_1.set'
raw = mne.io.read_raw_eeglab(set_file_path, preload=True)
print("Step 1: Raw Data Loaded (Before Marking Bad Channels)")
print(raw)


# Plot the raw data (time-domain view)
raw.plot(n_channels=64, title='Step 1: Before Marking Bad Channels', show=True)


# -----------------------------
# Step 2: Mark Bad Channels and Show the Data
# -----------------------------
# For example, mark 'Fp1' and 'Fz' as bad channels if they exist.
bad_channels = []
if 'Fp1' in raw.ch_names:
    bad_channels.append('FT10')

if bad_channels:
    raw.info['bads'] = bad_channels
    print("Step 2: Marked Bad Channels:", raw.info['bads'])
else:
    print("Step 2: No specified bad channels found to mark.")

# Plot the raw data again to reflect the bad channel markings
raw.plot(n_channels=64, title='Step 2: After Marking Bad Channels',bad_color='red', show=True)

# -----------------------------
# Step 3: Interpolate the Bad Channels and Show the Result
# -----------------------------
# Interpolate the bad channels using data from neighboring channels.
raw_interpolated = raw.copy().interpolate_bads(reset_bads=True)
print("Step 3: After Interpolation, bad channels reset to:", raw_interpolated.info['bads'])

# Plot the interpolated data to verify changes
raw_interpolated.plot(n_channels=64, title='Step 3: After Interpolation', show=True)



# Optional: Use input() to keep the script running (especially in some environments)
input("Press Enter to exit...")