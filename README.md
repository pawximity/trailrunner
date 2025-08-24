
## Trailrunner

Trailrunner is a lightweight CLI wrapper around psql for running ETL SQL scripts in Postgres/PostGIS. It’s designed to streamline execution of scripts in data/GIS workflows, with guardrails, sensible defaults and minimal overhead.

---

## Features

- Simple CLI interface for running scripts  
- Prompts for Postgres password if needed  
- Displays formatted command output and result  

---

## Requirements

- Python 3.8+
- `psql` (postgresql-client) installed and available on PATH
- PostGIS-enabled PostgreSQL database

Install Python dependencies:

```bash
pip install -r requirements.txt

