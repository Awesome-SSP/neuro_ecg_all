import os
import mne

# -----------------------------
# Step 1: Set Up Paths and Load Sample Evoked Data
# -----------------------------
# Get the sample data path (downloaded if not already available)
data_path = mne.datasets.sample.data_path()
subjects_dir = os.path.join(data_path, 'subjects')
subject = 'sample'

# Define the evoked file (auditory/visual evoked responses)
evoked_fname = os.path.join(data_path, 'MEG', 'sample', 'sample_audvis-ave.fif')

# Read the evoked response for condition 0 (e.g., Left Auditory)
evoked = mne.read_evokeds(evoked_fname, condition=0, baseline=(None, 0))
evoked = mne.read_evokeds(evoked_fname, condition=0, baseline=(None, 0))

print("Evoked response loaded.")

# Crop to a short time window for clearer visualization (e.g., 50-150 ms)
evoked.crop(0.05, 0.15)
# Plot the evoked response (no title parameter allowed)
fig = evoked.plot(time_unit='s')
# Set a title on the returned figure
fig.suptitle("Evoked Response (Auditory/Visual)")

# -----------------------------
# Step 2: Load Forward Solution and Noise Covariance
# -----------------------------
fwd_fname = os.path.join(data_path, 'MEG', 'sample', 'sample_audvis-meg-eeg-oct-6-fwd.fif')
fwd = mne.read_forward_solution(fwd_fname)
print("Forward solution loaded.")

cov_fname = os.path.join(data_path, 'MEG', 'sample', 'sample_audvis-cov.fif')
cov = mne.read_cov(cov_fname)
print("Noise covariance loaded.")

# -----------------------------
# Step 3: Create an Inverse Operator
# -----------------------------
inv_op = mne.minimum_norm.make_inverse_operator(evoked.info, fwd, cov, loose=0.2, depth=0.8)
print("Inverse operator created.")

# -----------------------------
# Step 4: Apply sLORETA to Compute the Source Estimate
# -----------------------------
# Use lambda2 = 1/9, approximating an SNR of about 3.
stc_sloreta = mne.minimum_norm.apply_inverse(evoked, inv_op, lambda2=1/9., method='sLORETA')
print("sLORETA source estimate computed.")

# -----------------------------
# Step 5: Visualize the sLORETA Source Estimate in 3D
# -----------------------------
# This opens an interactive 3D visualization window (requires a 3D backend, e.g., Mayavi)
stc_sloreta.plot(subject=subject, subjects_dir=subjects_dir, hemi='both', time_viewer=True)
input()