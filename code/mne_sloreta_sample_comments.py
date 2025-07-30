# %%

import os
import mne
# %%
# -----------------------------
# Step 1: Set Up Paths and Load Sample Evoked Data
# -----------------------------
# Get the sample data path (MNE sample dataset is used here).
data_path = mne.datasets.sample.data_path()
# Set the directory where subject-specific anatomical data are stored.
subjects_dir = os.path.join(data_path, 'subjects')
# 'sample' is the subject name provided with the sample dataset.
subject = 'sample'

# Define the filename for the evoked responses (auditory/visual experiment).
evoked_fname = os.path.join(data_path, 'MEG', 'sample', 'sample_audvis-ave.fif')

# Read the evoked response for condition 0 (typically "Left Auditory").
# The baseline correction is applied from the beginning up to time 0.
evoked = mne.read_evokeds(evoked_fname, condition=0, baseline=(None, 0))
print("Evoked response loaded.")

# Crop the evoked response to a short time window (50 to 150 ms) to focus on early responses.
# This helps in clearer visualization by reducing data length.
evoked.crop(0.05, 0.15)

# Plot the evoked response.
# The time unit is set to seconds for better interpretability.
fig = evoked.plot(time_unit='s')
# Since the 'plot' method does not accept a 'title' parameter, we set it on the returned figure.
fig.suptitle("Evoked Response (Auditory/Visual)")

# %%
# -----------------------------
# Step 2: Load Forward Solution and Noise Covariance
# -----------------------------
# Load the forward solution computed for the sample data.
# This forward model describes how brain sources project to the sensors.
fwd_fname = os.path.join(data_path, 'MEG', 'sample', 'sample_audvis-meg-eeg-oct-6-fwd.fif')
fwd = mne.read_forward_solution(fwd_fname)
print("Forward solution loaded.")

# Load the noise covariance matrix.
# This matrix characterizes the noise in the data and is used in the inverse solution.
cov_fname = os.path.join(data_path, 'MEG', 'sample', 'sample_audvis-cov.fif')
cov = mne.read_cov(cov_fname)
print("Noise covariance loaded.")

# %%
# -----------------------------
# Step 3: Create an Inverse Operator
# -----------------------------
# Create the inverse operator using:
# - evoked.info: sensor info from the evoked data.
# - fwd: forward solution.
# - cov: noise covariance.
# loose=0.2: Allows some freedom (20%) in the source orientation (non-fixed orientations).
# depth=0.8: Depth weighting, giving relatively more weight to deeper sources.
inv_op = mne.minimum_norm.make_inverse_operator(evoked.info, fwd, cov, loose=0.2, depth=0.8)
print("Inverse operator created.")

# %%
# -----------------------------
# Step 4: Apply sLORETA to Compute the Source Estimate
# -----------------------------
# sLORETA (standardized Low Resolution Brain Electromagnetic Tomography) is applied here.
# lambda2=1/9.: This regularization parameter is 1/SNR^2; with SNR ~3, lambda2 is approximately 1/9.
# method='sLORETA': Specifies the sLORETA method for inverse estimation.
stc_sloreta = mne.minimum_norm.apply_inverse(evoked, inv_op, lambda2=1/9., method='sLORETA')
print("sLORETA source estimate computed.")

# %%
# -----------------------------
# Step 5: Visualize the sLORETA Source Estimate in 3D
# -----------------------------
# This opens an interactive 3D visualization window.
# subject and subjects_dir help locate the MRI anatomy for the 'sample' subject.
# hemi='both' displays both left and right hemispheres.
# time_viewer=True enables a time viewer to explore the source dynamics.
stc_sloreta.plot(subject=subject, subjects_dir=subjects_dir, hemi='both', time_viewer=True)

# Optional: Use input() to keep the script running (especially in some environments)
input("Press Enter to exit...")

# %%
