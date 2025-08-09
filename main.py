import os
import json
import pandas as pd
import redis
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from datetime import datetime
from typing import List


r = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True)

app = FastAPI(title="Shoe API - Redis Only")



class DateInput(BaseModel):
    date: str  

class ColorInput(BaseModel):
    color: str



CSV_FILE = "fastapi/women_shoes.csv"

@app.on_event("startup")
def load_data_into_redis():
    if not os.path.exists(CSV_FILE):
        raise FileNotFoundError("CSV file not found")

    df = pd.read_csv(CSV_FILE)
    df.dropna(subset=['id', 'brand', 'colors', 'dateAdded'], inplace=True)

    for _, row in df.iterrows():
        try:
            shoe_id = str(row['id'])
            brand = str(row['brand'])
            colors = str(row['colors'])
            date_str = str(row['dateAdded'])

            timestamp = pd.to_datetime(date_str).timestamp()
            date_only = pd.to_datetime(date_str).strftime("%Y-%m-%d")

         
            r.hset(f"shoe:{shoe_id}", mapping={
                "id": shoe_id,
                "brand": brand,
                "colors": colors,
                "dateAdded": date_only
            })

           
            r.zadd(f"date:{date_only}", {shoe_id: timestamp})

        
            for color in colors.split(","):
                color_clean = color.strip().lower()
                r.zadd(f"color:{color_clean}", {shoe_id: timestamp})

        except Exception as e:
            continue  



@app.get("/")
def root():
    return {"message": "Welcome to Redis-only Shoe API"}


@app.post("/shoe/most-recent")
def get_most_recent_shoe(input: DateInput):
    date_key = f"date:{input.date}"
    ids = r.zrevrange(date_key, 0, 0)

    if not ids:
        raise HTTPException(status_code=404, detail="No shoes found for this date")

    shoe_data = r.hgetall(f"shoe:{ids[0]}")
    return shoe_data


@app.post("/shoe/by-date")
def get_all_shoes_by_date(input: DateInput):
    date_key = f"date:{input.date}"
    ids = r.zrevrange(date_key, 0, -1)

    if not ids:
        raise HTTPException(status_code=404, detail="No shoes found for this date")

    shoes = [r.hgetall(f"shoe:{shoe_id}") for shoe_id in ids]
    return {"date": input.date, "total": len(shoes), "shoes": shoes}


@app.post("/shoe/by-color")
def get_shoes_by_color(input: ColorInput):
    color_key = f"color:{input.color.strip().lower()}"
    ids = r.zrevrange(color_key, 0, -1)

    if not ids:
        raise HTTPException(status_code=404, detail="No shoes found for this color")

    shoes = [r.hgetall(f"shoe:{shoe_id}") for shoe_id in ids]
    return {"color": input.color, "total": len(shoes), "shoes": shoes}