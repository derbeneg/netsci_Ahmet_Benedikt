Open your terminal (e.g., VS Code Terminal or Mac Terminal), and run:
 
# ------------------------ (run all commands separately)

git clone https://github.com/derbeneg/netsci_Ahmet_Benedikt.git
cd netsci_Ahmet_Benedikt

python3 -m venv .venv          # Create virtual environment
source .venv/bin/activate      # Activate it (or .venv\Scripts\activate on Windows)
pip install -r requirements.txt

pip install -r requirements.txt

# ------------------------


📁 Project Folder Overview

netsci_Ahmet_Benedikt/
├── data/         ← Put data files here (folder is empty by default)
├── notebooks/    ← Jupyter notebooks go here
├── outputs/      ← Plots and results
├── src/          ← Python helper scripts
├── requirements.txt
└── README.md

# Note: The data/ folder is not tracked by Git (on purpose) — you’ll need to add your own data files locally.

# Later for pulling new changes:
git pull origin main

