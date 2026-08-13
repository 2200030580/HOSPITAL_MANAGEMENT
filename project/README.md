# Hospital Appointment Management API

## Quick start

Install dependencies:

```bash
python -m pip install -r requirements.txt
```

Create database tables:

```bash
python create_tables.py
```

Run locally:

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Run tests:

```bash
pytest -q
```

Docker build:

```bash
docker build -t hospital-api .
docker run -p 8000:8000 hospital-api
```
