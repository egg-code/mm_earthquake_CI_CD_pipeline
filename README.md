# 🌍 Earthquake ETL Pipeline

A Python-based ETL pipeline that fetches earthquake data from the [USGS Earthquake API](https://earthquake.usgs.gov/fdsnws/event/1/), transforms it, and loads it into a PostgreSQL database. Built to track seismic activity within a 600 km radius of central Myanmar.

## 🚀 Features

- Extracts earthquake data from the USGS API (live data)
- Filters out previously loaded earthquake events by ID
- Transforms raw GeoJSON data into a clean, structured DataFrame
- Loads transformed data into a PostgreSQL database (e.g., [Neon](https://neon.tech/))
- Logs key actions and errors for traceability

## 🛠 Technologies Used

- Python
- `pandas`, `sqlalchemy`, `psycopg2`
- PostgreSQL (hosted or local)
- USGS Earthquake API
- Git for version control
- GitHub Actions (optional CI/CD)

## 📁 Project Structure

```bash
.
├── main.py                # Main ETL execution script
├── models.py              # SQLAlchemy ORM model (Earthquake)
├── etl_utils.py           # Custom classes: Extract, Transform, Load, Saveids, Loadids
├── ids.txt                # Local cache of processed earthquake IDs
├── requirements.txt       # Python dependencies
└── README.md              # Project documentation
KaungMyatKyaw(egg)
