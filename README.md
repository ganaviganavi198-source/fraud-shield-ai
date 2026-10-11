# Fraud Shield AI

A Flask web app that checks transactions for fraud risk. Each transaction is labeled **safe**, **medium**, or **high** risk, and a dashboard shows the recent transaction history and a risk timeline.

## Features

- Check a transaction and see its risk level on a result page
- Dashboard with recent transactions and their risk labels
- Timeline chart of checks over time, with risk scores
- Results saved in a local SQLite database (`fraudshield.db`)

## Project structure

- `app.py`: Flask server, detection logic, and database access
- `Templates/dashboard.html`: the dashboard page
- `Templates/fraud_detection.html`: the transaction input form
- `Templates/result.html`: the risk result page
- `requirements.txt`: Python packages the project needs

## Setup

```
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

## Run

```
python app.py
```

Then open http://127.0.0.1:5000/dashboard in your browser. Press `Ctrl + C` in the terminal to stop the server.

## How detection works

[Describe your method here, for example: "Each transaction is scored using rules based on amount, time of day, and transaction frequency. Scores above X are high risk."]

## Notes

- The database file is created on your computer when the app runs. It is not uploaded to GitHub.
- The app runs locally. GitHub stores the code, but it does not run the app.