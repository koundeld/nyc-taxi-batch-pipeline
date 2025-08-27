# NYC Taxi Batch Pipeline (Spark → BigQuery)

## 📌 Overview
This project demonstrates a **batch data pipeline** that ingests NYC Yellow Taxi trip records, processes them with **Apache Spark (PySpark)**, and writes aggregated results into **Google BigQuery** for downstream analytics.  

The goal is to showcase an **end-to-end data engineering workflow** with scalable Spark jobs and cloud-native storage.

---

## ⚙️ Architecture

Raw CSV (NYC Taxi Data)
↓
Spark (PySpark job)
↓
Curated Data (aggregated hourly fares)
↓
Google BigQuery (analytics-ready)

---

## 🛠 Tech Stack
- **Apache Spark 3.4** (installed via Homebrew, PySpark API in Python)
- **Google BigQuery** (data warehouse, analytics-ready target)
- **Python 3.10** (venv)
- **Airflow 2.9** → Orchestration for scheduling pipeline runs

---

## 📂 Project Structure
```
.
├── data/
│   ├── raw/                  # Sample taxi trip data (tiny CSV or empty with .gitkeep)
│   └── curated/              # Spark outputs (ignored in Git, .gitkeep to keep folder)
│
├── jobs/
│   └── nyc_batch.py          # PySpark batch job
│
├── dags/
│   └── nyc_taxi_dag.py       # Airflow DAG (orchestration)
│
├── .gitignore                # Git ignore rules
└── README.md                 # Project documentation
---
```

## 🚀 Pipeline Steps
1. **Data Ingestion**  
   - Downloaded sample **NYC Yellow Taxi** CSV data (~50k rows).  
   - Data stored locally under `data/raw/`.

2. **Transformation with Spark**  
   - PySpark job reads CSV.  
   - Performs aggregation of total fares **per pickup hour**.  
   - Writes output to `data/curated/hourly_fares/`.  

3. **Load to BigQuery**  
   - Curated parquet files loaded into BigQuery.  
   - Table partitioned by pickup hour for efficient queries.  

4. **Analytics**  
   - Run SQL queries on BigQuery (e.g., highest fares per hour).  
---

## ▶️ Running Locally
**Run Spark job directly:**
```
	bash spark-submit --master "local[*]" jobs/nyc_batch.py data/raw/yellow_tripdata_sample.csv data curated/hourly_fares
```
---

## ⏱ Orchestration with Airflow (Optional)
	•	Airflow can schedule and monitor the Spark job.
	•	A DAG (nyc_taxi_dag.py) triggers the PySpark job on a daily schedule.
	•	Provides retries, logging, and UI-based monitoring.
	👉 See /dags/nyc_taxi_dag.py for details.
---

## 📊 Sample Output (BigQuery)
```
Row	pickup_hour	trips	avg_fare
1	0	13	10.76923076923077
2	1	10	21.401
3	2	5	20.1
4	4	3	35.54
```
---

## 🔧 Challenges & Learnings
	•	GCP Project ID is required to set at environment level.
	•	Installing dependencies jar gcs-connector-hadoopX.jar and spark-bigquery-with-dependenciesX.jar
	•	Isolated dependencies inside .venv (Airflow + PySpark).
