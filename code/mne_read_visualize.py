import mne

set_file_path = 's17_1.set'
raw = mne.io.read_raw_eeglab(set_file_path, preload=True)

print("Raw Data: ",raw)
print("Dataset Info: ",raw)

raw.plot(n_channels=63, title='Raw Data: Before Filtering')


# Optional: Use input() to keep the script running (especially in some environments)
input("Press Enter to exit...")