import os
import mne
from mne.preprocessing import ICA, create_eog_epochs
import matplotlib.pyplot as plt

# ------------------------------------------------------------------
# Step 1: Load the EEG Data (EEGLAB .set file)
# ------------------------------------------------------------------

set_file_path = 's17_1.set'

raw = mne.io.read_raw_eeglab(set_file_path, preload=True)
print("Raw Data Loaded:")
print(raw)

# Plot raw data to inspect time-domain signals
raw.plot(n_channels=64, title='Raw Data: Before Preprocessing', show=True)

# ------------------------------------------------------------------
# Step 2: Set a Standard Montage
# ------------------------------------------------------------------
# Setting a standard montage assigns typical electrode positions.
# "standard_1020" is commonly used for EEG data.
montage = mne.channels.make_standard_montage('standard_1020')
raw.set_montage(montage, on_missing='warn')
print("Montage set to standard_1020.")

# ------------------------------------------------------------------
# Step 3: Filtering (Bandpass 1-40 Hz)
# ------------------------------------------------------------------
# Bandpass filtering between 1 and 40 Hz removes slow drifts and high-frequency noise.
raw_filtered = raw.copy().filter(l_freq=1, h_freq=40, fir_design='firwin')
print("Bandpass filtering applied (1-40 Hz).")
raw_filtered.plot(n_channels=64, title='Filtered Data (1-40 Hz)', show=True)


# ------------------------------------------------------------------
# Step 4: Mark Bad Channels
# ------------------------------------------------------------------
# Identify channels with poor quality.
# In this example, we assume 'Fp1' and 'Fz' are noisy (adjust based on your visual inspection).
bad_channels = []
if 'Fp1' in raw_filtered.ch_names:
    bad_channels.append('Fp1')
if 'Fz' in raw_filtered.ch_names:
    bad_channels.append('Fz')

if bad_channels:
    raw_filtered.info['bads'] = bad_channels
    print("Marked Bad Channels:", raw_filtered.info['bads'])
else:
    print("No bad channels found to mark.")

# Plot to visualize bad channels (they appear in red in MNE plots)
raw_filtered.plot(n_channels=64, title='After Marking Bad Channels', bad_color='red', show=True)


# ------------------------------------------------------------------
# Step 5: Artifact Correction Using ICA
# ------------------------------------------------------------------
# Initialize ICA:
# - n_components=20: Decompose the data into 20 independent components.
# - random_state=97: For reproducibility.
# - max_iter='auto': Let MNE decide the number of iterations.
ica = ICA(n_components=20, random_state=97, max_iter='auto')
ica.fit(raw_filtered)
print("ICA fitted on filtered data.")

# Optionally, use an EOG channel to help identify eye blink artifacts:
if 'EOG' in raw_filtered.ch_names:
    eog_epochs = create_eog_epochs(raw_filtered, ch_name='EOG')
    eog_inds, scores = ica.find_bads_eog(eog_epochs)
    print("Detected EOG-related ICA components:", eog_inds)
    ica.exclude = eog_inds
else:
    # If no EOG channel is available, inspect components visually.
    # Here, for demonstration, we assume components 0 and 3 are artifacts.
    ica.exclude = [0, 3]
    print("Manually marked components [0, 3] as artifacts.")


# Apply ICA to remove artifact components and reconstruct the clean signal.
raw_clean = raw_filtered.copy()
ica.apply(raw_clean)
print("ICA applied; artifacts removed.")
raw_clean.plot(n_channels=64, title="Cleaned Data after ICA", show=True)


# ------------------------------------------------------------------
# Step 6: Epoching (Optional)
# ------------------------------------------------------------------
# Convert annotations to events. This will create an event array from annotations.
events, event_id = mne.events_from_annotations(raw_clean)
print("Event IDs from annotations:", event_id)
print("Total events detected:", len(events))


# If you have a specific condition (e.g., "Encoding") in your annotations,
# extract epochs for that condition. (Adjust the condition name as needed.)
if "Encoding" in event_id:
    tmin = -0.2  # 200 ms before the event
    tmax = 0.8   # 800 ms after the event
    baseline = (None, 0)  # Baseline correction using pre-stimulus period
    epochs = mne.Epochs(raw_clean, events, event_id=event_id, tmin=tmin, tmax=tmax,
                        baseline=baseline, preload=True)
    epochs_encoding = epochs["Encoding"]
    print("Epochs for 'Encoding' condition:")
    print(epochs_encoding)
    # Plot a few epochs to inspect
    epochs_encoding.plot(n_epochs=5, n_channels=64, title="Epochs: Encoding Condition", show=True)
else:
    print("No 'Encoding' event found; skipping epoching.")

# ------------------------------------------------------------------
# Step 7: Save Preprocessed Data (Optional)
# ------------------------------------------------------------------
# Save the cleaned data for later use.
preprocessed_file = r'C:\Users\harsh\Downloads\data\s17_1_preprocessed.fif'
raw_clean.save(preprocessed_file, overwrite=True)
print("Preprocessed data saved at:", preprocessed_file)

input("press ctrl+c to exit")