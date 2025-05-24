Open your terminal (e.g., VS Code Terminal or Mac Terminal), and run:
 
# ------------------------ (run all commands separately)

git clone https://github.com/derbeneg/netsci_Ahmet_Benedikt.git
cd netsci_Ahmet_Benedikt

python3 -m venv .venv          # Create virtual environment
source .venv/bin/activate      # Activate it (or .venv\Scripts\activate on Windows)
pip install -r requirements.txt
pip install -e .


# ------------------------


📁 Project Folder Overview

netsci_Ahmet_Benedikt/
├── data/                     ← raw CSVs & pickles go here (tracked with .gitkeep)
│   ├── .gitkeep
│   └── clean/                ← cleaned pickles + graph_cache
│       ├── .gitkeep
│       └── graph_cache/
│           └── .gitkeep
├── scripts/                  ← data-pull, preprocess, graph_utils, helpers
│   ├── fetch_pepe_etherscan.py
│   ├── preprocess.py
│   └── graph_utils.py
├── notebooks/                ← one notebook per analysis point
│   ├── 01_degree_distribution.ipynb
│   ├── 02_global_summaries.ipynb
│   └── …  
├── outputs/                  ← auto-saved figures, tables, exports
├── insights/                 ← write-ups, mini-reports, markdown notes
│   └── 01_initial_report.md
├── ANALYSIS_PLAN.md          ← this roadmap of analysis → hypothesis mapping
├── requirements.txt          ← minimal dependencies
├── .gitignore                ← ignores data files, caches, venv, etc.
└── README.md                 ← setup & run instructions


# Note: The data/ folder is not tracked by Git (on purpose) — you’ll need to add your own data files locally.

# Later for pulling new changes:
git pull origin main

