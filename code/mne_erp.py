import os
import mne
import matplotlib.pyplot as plt

# ------------------------------------------------------------------
# Step 1: Load EEG Data from an EEGLAB (.set) File
# ------------------------------------------------------------------
# Use a raw string to avoid escape issues in Windows file paths.
set_file_path = 's17_1.set'
raw = mne.io.read_raw_eeglab(set_file_path, preload=True)
print("Raw Data Loaded:")
print(raw)

# Plot the raw data (time-domain view) to visually inspect the data.
raw.plot(n_channels=64, title='Raw Data: Before Epoching', show=True)

# ------------------------------------------------------------------
# Step 2: Convert Annotations to Events
# ------------------------------------------------------------------
# Convert the annotations (e.g., "Encoding", "Recall", etc.) into an event array.
events, event_id = mne.events_from_annotations(raw)
print("Event IDs found:", event_id)
print("Total events detected:", len(events))

# ------------------------------------------------------------------
# Step 3: Create Epochs for a Specific Condition (e.g., "Encoding")
# ------------------------------------------------------------------
# Ensure the condition "Encoding" exists in event_id.
if "Encoding" not in event_id:
    raise ValueError("No 'Encoding' event found in annotations. Available events: {}".format(event_id))

# Define epoch parameters:
tmin = -0.2  # Start time: 200 ms before the event
tmax = 0.8   # End time: 800 ms after the event
baseline = (None, 0)  # Baseline correction: from the beginning of the epoch up to time 0

# Create epochs using all detected events.
epochs = mne.Epochs(raw, events, event_id=event_id, tmin=tmin, tmax=tmax,
                    baseline=baseline, preload=True)
print("Epochs created.")

# Extract epochs specifically for the "Encoding" condition.
epochs_encoding = epochs["Encoding"]
print("Epochs for 'Encoding':", epochs_encoding)

# Visualize a few epochs to inspect their quality.
epochs_encoding.plot(n_epochs=5, n_channels=64, title="Epochs: Encoding Condition", show=True)

# ------------------------------------------------------------------
# Step 4: Compute the Evoked Response (ERP)
# ------------------------------------------------------------------
# Average the epochs to compute the ERP for the "Encoding" condition.
evoked_encoding = epochs_encoding.average()
print("Evoked response for 'Encoding' computed.")

# Plot the ERP. Since the plot() function does not accept a title parameter directly,
# we set the title on the returned figure.
fig = evoked_encoding.plot(time_unit='s')
fig.suptitle("Evoked Response (ERP) for Encoding Condition")
plt.show()

# Optional: Use input() to keep the script running (especially in some environments)
input("Press Enter to exit...")


"""
Explanation:

ERP kya hai?
ERP, yaani Event-Related Potential, wo average brain response hai jo aapke EEG mein dikhai deta hai jab koi stimulus present hota hai. Matlab, jab aap bar-bar ek hi experiment karte hain, to har trial ka signal thoda noisy hota hai. Par jab in signals ko average kar diya jata hai, to consistent patterns (jaise P300, N100, etc.) saamne aate hain.

Use:
ERP se aapko pata chalta hai ki aapka brain kisi specific event par kaise react karta hai. Ye cognitive processes aur sensory processing samajhne mein help karta hai.


Loading Data:

    The EEG data is loaded from a specified EEGLAB file using mne.io.read_raw_eeglab() with preload=True to load all data into memory.

    A time-domain plot is generated to inspect the raw signals before further processing.

    Converting Annotations to Events:

    The annotations (labels like "Encoding", "Recall", etc.) in the raw data are converted to events using mne.events_from_annotations().

    The event IDs and the total number of events are printed.

Epoching:

    Epochs are created from the continuous data around each event (from –200 ms to 800 ms).

    Baseline correction is applied using the pre-stimulus interval (from the beginning of the epoch to 0 s).

    Epochs corresponding to the "Encoding" condition are extracted and plotted to verify quality.

Computing ERP:

    The ERP is computed by averaging the epochs for the "Encoding" condition.

    The evoked response (ERP) is then plotted interactively. The title is added to the plot after it is generated.

"""