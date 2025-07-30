from mne.datasets import eegbci
import os
from mne.io import read_raw_edf

# Download EEGBCI data for subject 1 and motor imagery runs (e.g., runs 4, 8, 12)
eeg_data_paths = eegbci.load_data(subject=1, runs=[4, 8, 12])
print("Downloaded EEGBCI file paths:")
for path in eeg_data_paths:
    print("  ", path)


# Select one of the downloaded files for demonstration
raw_file = eeg_data_paths[0]
print("Reading EEG file:", os.path.basename(raw_file))

# Read the EEG data (preload=True loads the data into memory for faster processing)
raw = read_raw_edf(raw_file, preload=True)
print("Raw EEG data info:")
print(raw)

print("\nDataset Inforrmation",raw.info)

# Optional: Use input() to keep the script running (especially in some environments)
input("Press Enter to exit...")