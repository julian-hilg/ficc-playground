Research platform for FICC

## Architecture
```
Research (Jupyter) → Core Library (Python) → API (FastAPI) → Dashboard (React)
```
## Quick Start
```bash

# Everyone clones repo
git clone https://github.com/julian-hilg/ficc-playground.git

cd ficc-playground


# Install dependencies
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Start Jupyter research environment
cd research
jupyter notebook
# OR
jupyter lab

# Start API server (in another terminal) -- LATER, when frontend is implemented
uvicorn ficc.api:app --reload
# Start React dashboard (in another terminal)
cd dashboard
npm install
npm start


# Create feature branch (examplary)
git checkout -b feature/yield-curves

# Make changes, commit
git add .
git commit -m "Add Nelson-Siegel curve fitting"

# Push and open PR
git push origin feature/yield-curves
# Open PR on GitHub for review


```

## Modules

- **Bond Analytics** - Pricing, duration, convexity, DV01
- **Yield Curves** - Bootstrapping, interpolation (tbd)
## Tech Stack

- **Research**: Jupyter, NumPy, Pandas, Matplotlib
- **Backend**: FastAPI, QuantLib, YFinance
- **Frontend**: React, Recharts, Tailwind CSS
- **Deployment**: Docker, AWS

## Code Style

Follow PEP 8 with these tools:

```bash
# Format code (line length 100)
black --line-length 100 ficc/

# Sort imports
isort ficc/

# Combined command
black --line-length 100 ficc/ && isort ficc/
```

**Standards**:
- Line length: 100 characters
- Imports: stdlib → third-party → local
- Type hints required for all functions
- Docstrings: one-line summary only
- No verbose comments in code
- Dictionary returns for all analytics functions
