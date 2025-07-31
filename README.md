# 📄 EEG Brain Mastery

## 🧠 MNE EEG Workshop - Brain Signal Processing with Python

This repository contains a collection of Jupyter notebooks and Python scripts for EEG data analysis using the **MNE-Python** library. It provides hands-on examples for preprocessing, visualization, ERP analysis, ICA, and advanced source localization techniques like dSPM and sLORETA.

---

## 📁 Contents

| File | Description |
|------|-------------|
| `Mne_Workshop.ipynb` | Main Jupyter notebook showcasing EEG analysis pipeline using MNE |
| `mne_bad_channel.py` | Detects and marks bad EEG channels for interpolation or exclusion |
| `mne_dspm_loreta.py` | Applies dSPM and LORETA for EEG source localization |
| `mne_epoching.py` | Segments continuous EEG data into epochs based on events |
| `mne_erp.py` | Computes and visualizes event-related potentials (ERPs) |
| `mne_filters.py` | Applies bandpass/bandstop filters to EEG signals |
| `mne_filters_psd.py` | Computes and plots power spectral density (PSD) after filtering |
| `mne_ica.py` | Runs Independent Component Analysis to remove artifacts like EOG/EMG |
| `mne_preprocessing_pipeline.py` | Combines multiple preprocessing steps into a unified pipeline |
| `mne_read_visualize.py` | Loads raw EEG data and provides basic visualizations |
| `mne_rereferencing.py` | Applies EEG rereferencing techniques (e.g., average, mastoids) |
| `mne_sample_data.py` | Demonstrates loading and using MNE's sample EEG dataset |
| `mne_sloreta_sample_comments.py` | Adds anatomical or functional labels to sLORETA results |
| `sloreta_sample.py` | Basic example of sLORETA source localization using sample data |
| `st1.py` | (TBD) Auxiliary script for experiment or test processing |
| `time_vs_freq.py` | Compares EEG in time-domain vs frequency-domain analysis |
| `s17_1.set`, `s17_1.fdt` | Raw EEG data in EEGLAB format (used in analysis) |

---

## ⚙️ Requirements

Install dependencies using:

```bash
pip install mne numpy matplotlib scipy jupyter
```

🚀 Getting Started
Open Mne_Workshop.ipynb in Jupyter

Follow the step-by-step code to preprocess and analyze EEG data

Explore individual .py scripts to deep dive into specific techniques

---

🎯 Goals of the Project
Teach EEG preprocessing techniques using Python & MNE

Visualize time-domain and frequency-domain EEG

Perform ERP and ICA-based artifact rejection

Introduce dSPM & sLORETA for source localization
 
---
📚 References
MNE-Python Documentation

EEGLAB Dataset Format

Neuroimaging in Python

🧠 Citation
If this repository helps your learning or research, please consider citing the MNE-Python library or referencing this project in your work.

---

🤝 Contributing
Pull requests and suggestions are welcome! Open issues for enhancements or bugs.

## Authors

- [@SSP](https://github.com/Awesome-SSP)

## Support

For support, you can buy me a coffee

<a href="https://buymeacoffee.com/i.awesomessp" target="_blank"><img src="https://cdn.buymeacoffee.com/buttons/default-orange.png" alt="Buy Me A Coffee" height="41" width="174"></a>
