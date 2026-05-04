# Auto Job Applier

This project uses agentic AIs to extract job preferences from a user CV and aggregate job postings that match.

## Project Structure

```
├── src
│   ├── main.py        # Orchestrator
│   ├── models.py      # Pydantic schemas (Data Contracts)
│   ├── analyzer.py    # AI Profile Analyzer (Step 1)
│   └── sourcer.py     # Job Sourcer API (Step 2)
├── requirements.txt   # Python Dependencies
└── .env.example       # API Key configuration
```

## Getting Started

1. Create a virtual environment: `python -m venv venv`
2. Activate the environment: `source venv/bin/activate`
3. Install dependencies: `pip install -r requirements.txt`
4. Copy `.env.example` to `.env` and set your variables.
5. Run the main file: `python -m src.main`
