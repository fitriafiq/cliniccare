# ClinicCare

## Backend + database

```bash
cd backend
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

# run the API (this also creates the database tables on first run)
uvicorn app.main:app --reload
```

Then, in a separate terminal, load the sample diagnosis codes (first time only):

```bash
cd backend
sqlite3 cliniccare.db < data/seed.sql
```

Backend runs at http://localhost:8000 (docs at http://localhost:8000/docs).

## Frontend

```bash
cd frontend
pnpm install
pnpm dev
```

Frontend runs at http://localhost:3000.
