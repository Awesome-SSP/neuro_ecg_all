import os
import mne

# ------------------------------------------------------------------
# Step 1: Load the EEG Data (EEGLAB .set file)
# ------------------------------------------------------------------
# Use a raw string for the file path to avoid escape issues.
set_file_path = 's17_1.set'
raw = mne.io.read_raw_eeglab(set_file_path, preload=True)
print("Raw Data Loaded:")
print(raw)

# Plot raw data for a visual inspection of time-domain signals
raw.plot(n_channels=64, title='Raw Data: Before Epoching', show=True)

# ------------------------------------------------------------------
# Step 2: Convert Annotations to Events
# ------------------------------------------------------------------
# This converts the annotations (e.g., "Encoding", "Recall", etc.) into an event array.
events, event_id = mne.events_from_annotations(raw)
print("Event IDs found:", event_id)
print("Number of events detected:", len(events))

# ------------------------------------------------------------------
# Step 3: Create Epochs for a Specific Condition (e.g., "Encoding")
# ------------------------------------------------------------------
# Check if "Encoding" is available in the event IDs; if not, raise an error.
if "Encoding" not in event_id:
    raise ValueError("No 'Encoding' event found in the annotations. Available events: {}".format(event_id))

# Define epoch parameters:
tmin = -0.2  # Start time: 200 ms before the event
tmax = 0.8   # End time: 800 ms after the event
baseline = (None, 0)  # Use data from before the event for baseline correction

# Create epochs for all conditions using the events array and event_id dictionary.
epochs = mne.Epochs(raw, events, event_id=event_id, tmin=tmin, tmax=tmax,
                    baseline=baseline, preload=True)
print("Epochs created.")
# Extract epochs specifically for the "Encoding" condition.
epochs_encoding = epochs["Encoding"]
print("Epochs for 'Encoding':")
print(epochs_encoding)

# Plot a few epochs for the "Encoding" condition to inspect them.
epochs_encoding.plot(n_epochs=5, n_channels=64, title="Epochs: Encoding Condition", show=True)

# ------------------------------------------------------------------
# Step 4: Compute the Evoked Response (ERP)
# ------------------------------------------------------------------
# Average the epochs for the "Encoding" condition to compute the ERP.
#evoked_encoding = epochs_encoding.average()
#print("Evoked response for 'Encoding' computed.")

# Plot the evoked response.
#fig = evoked_encoding.plot(time_unit='s')
#fig.suptitle("Evoked Response: Encoding Condition")


# Optional: Use input() to keep the script running (especially in some environments)
input("Press Enter to exit...")






"""
Explanation:

Loading Data:

    The EEG data is loaded from an EEGLAB file using read_raw_eeglab() with preload=True for fast processing.

    The raw data is plotted to inspect the EEG signals in the time domain.

    Converting Annotations to Events:

    The function mne.events_from_annotations() extracts events from the data’s annotations. These events correspond to various experimental conditions like "Encoding", "Recall", etc.

Epoch Creation:

    Epochs are created using the detected events and a specified time window (tmin = -0.2 s to tmax = 0.8 s).

    Baseline correction is applied using data from before the event (up to 0 s).

    Epochs specific to the "Encoding" condition are extracted and plotted to verify their quality.

Evoked Response:

    The evoked response (ERP) is computed by averaging the epochs of the "Encoding" condition.

    The ERP is plotted with a title set using the returned figure.


"""