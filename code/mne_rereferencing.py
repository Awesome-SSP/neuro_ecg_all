import mne

# Load your EEG data from an EEGLAB .set file
set_file_path = 's17_1.set'
raw = mne.io.read_raw_eeglab(set_file_path, preload=True)
print("Raw Data:")
print(raw)

# Plot the raw data before re-referencing for comparison
raw.plot(n_channels=10, title='Raw Data: Before Re-referencing')

# ------------------------------------------------------------------
# Perform Average (Common) Re-referencing
# ------------------------------------------------------------------
# The 'set_eeg_reference' function with ref_channels='average' computes
# the average across all EEG channels and subtracts it from each channel.
raw_avg_ref = raw.copy().set_eeg_reference(ref_channels='average')

# Explanation:
# - "raw.copy()" creates a copy of the raw data so that the original remains unchanged.
# - "set_eeg_reference(ref_channels='average')" computes the mean across all EEG channels and
#   subtracts that average from each channel, resulting in a common average reference.
raw_avg_ref.plot(n_channels=10, title='EEG Data After Average Re-referencing')


# Optional: Use input() to keep the script running (especially in some environments)
input("Press Enter to exit...")