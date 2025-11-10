Research platform for FICC

## Architecture
```
Research (Jupyter) → Core Library (Python) → API (FastAPI) → Dashboard (React)
```
## Quick Start
```bash
# Install dependencies
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Start Jupyter research environment
cd research
jupyter notebook

# Start API server (in another terminal)
uvicorn ficc.api:app --reload
# Start React dashboard (in another terminal)
cd dashboard
npm install
npm start
```

## Modules

- **Bond Analytics** - Pricing, duration, convexity, DV01
- **Yield Curves** - Bootstrapping, interpolation
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
