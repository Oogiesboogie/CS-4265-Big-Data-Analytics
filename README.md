# Lap by Lap: Formula 1 Telemetry and Race Analytics

## Overview

This project builds a scalable Big Data pipeline that processes multi-season Formula 1 telemetry and race data using Apache Spark and FastF1 APIs 

It extracts, processes, and analyzes race performance data to generate driver and race-level insights across multiple seasons. 

---

## What It Does
- Ingests Formula 1 race and qualifying data across multiple seasons
- Processes telemetry using distributed Spark transformations
- Generates performance analytics such as:
  - Driver average lap times
  - Fastest laps per race
  - Race pace comparisons
- Validates data quality before output
- Produces structured analytical datasets

---

## Architecture 

**Pipeline Flow:**

Date Sources (FastF1 API)
-> Ingestion Layer
-> Spark Processing Layer
-> Feature Engineering
-> Validation Layer
-> Output (Parquet files)

---

## Technology Stack
- Python 3.12
- Apache Spark (PySpark)
- JSON (raw ingestion)
- CSV (some telemetry input (FastF1))
- Parquet (analytical storage format)
  
---

## Project Structure

CS-4265-Big-Data-Analytics/\
│\
├── src/\
│ ├── main.py\
│ │\
│ ├── ingestion/\
│ │ ├── openf1.py\
│ │ └── fastf1.py\
│ │\
│ ├── processing/\
│ │ ├── transform.py\
│ │ └── features.py\
│ │\
│ ├── validation/\
│ │ └── validate.py\
│\
├── data/\
│ └── sample/\
│\
├── output/\
│ └── (generated results)\
│\
├── docs/\
│ ├── M4_Final_Report.pdf\
│ ├── validation.md\
│ └── architecture.png\
│\
├── requirements.txt\
├── .gitignore\
├── .env.example\
├── LICENSE\
└── README.md

---
## Setup Instructions
git clone https://github.com/YOUR_USERNAME/CS-4265-Big-Data-Analytics.git
cd CS-4265-Big-Data-Analytics

Create virtual environment:
python -m venv .venv

Activate environment:
Windows: .venv\Scripts\activate  
Mac/Linux: source .venv/bin/activate

Install dependencies:
pip install -r requirements.txt

Run pipeline:
python src/main.py

## 📦 Data Schema & Outputs

This pipeline processes both raw and transformed datasets.

---

### 🗂️ Raw Data Inputs

| File | Description | Format |
|------|-------------|--------|
| 2025_sessions.json | OpenF1 session metadata | JSON |
| 2018_bahrain_laps.csv | FastF1 lap timing data | CSV |
| 2018_bahrain_results.csv | FastF1 official race results | CSV |

---

### ⚙️ Processed Data Outputs

| Dataset | Description | Format | Notes |
|----------|-------------|--------|-------|
| openf1_sessions | Cleaned OpenF1 session data | Parquet | FullName, Team, Event, SessionType, LapTime |
| fastf1_laps | Cleaned lap-by-lap telemetry | Parquet | Driver, LapNumber, LapTime, RaceName |
| fastf1_results | Final race classification data | Parquet | Driver, Position, Points, Team |

---

### 📊 Sample Output Metrics

- OpenF1 processed rows: ~120  
- FastF1 lap records: ~90  
- FastF1 results records: ~22  

---

### 🧾 Sample Records

#### OpenF1 Processed Data

| FullName | Team | Event | SessionType | LapTime |
|----------|------|-------|-------------|---------|
| Lando Norris | McLaren | Bahrain GP | Race | 1:34.123 |
| Max Verstappen | Red Bull | Bahrain GP | Race | 1:34.567 |

---

#### FastF1 Lap Data

| Driver | LapNumber | LapTime | RaceName |
|--------|-----------|---------|----------|
| Lando Norris | 1 | 1:34.123 | Bahrain GP |
| Max Verstappen | 1 | 1:34.567 | Bahrain GP |

---

## Data Validation 

The pipeline includes:
- Null checks on critical fields
- Empty dataset validation
- Schema verification
- Basic statistical sanity checks

---

## Known Limitations

- Dataset size depends on FastF1 API availability
- Local Spark performance varies by machine
- Cache files are excluded from version control
- Some historical data may be incomplete

---

## Future Improvements

- Expand to full multi-season ingestion
- Add streaming real-time telemetry pipeline
- Build visualization dashboard (Plotly / Power BI)
- Deploy to cloud (AWS / Databricks / GCP)
- Add predictive machine learning models

---

## Cache Handling

FastF1 generates local cache files which are not tracked in Git.

To clear cache if needed:
rm -rf data/cache

--- 

## Dependencies

Required packages:
- pyspark
- fastf1
- pandas
- requests

Install with:
pip install -r requirements.txt

---

## License

MIT License

--- 

## Project Summary

This project demonstrates:
- Distributed data processing using Spark
- API-based ingestion pipeline design
- Data transformation and feature engineering
- Data validation and quality control
- Scalable architecture for analytics workflows
