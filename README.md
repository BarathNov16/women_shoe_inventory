Shoe API — FastAPI + Redis

This project is a simple FastAPI + Redis API that loads shoe data from a CSV file and serves it through REST endpoints. On startup, the CSV is read and stored in Redis using hashes and sorted sets for quick access. Each shoe is indexed by ID, date, and color, making it easy to query.

You can fetch the most recent shoe for a given date, get all shoes added on a specific date, or list all shoes by color. The API runs on uvicorn and requires Redis to be running locally.

Setup is quick: install dependencies with pip install fastapi uvicorn redis pandas, start Redis, and then run uvicorn main:app --reload. Interactive API docs are available at /docs once the server is running.

This project demonstrates a clean ETL ,Redis ,API ,JSON flow using only FastAPI and Redis, without an SQL database.
