from fastapi import FastAPI, HTTPException
import redis
from schemas import Data
from config import REDIS_HOST, REDIS_PORT # данные для подключения храним в .env


app = FastAPI()
redis_client = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, db=0)


# ручка для записи данных в Redis
@app.post("/write_data")
async def write_data(data: Data):
    redis_client.set(data.phone, data.address)
    return {"message": "Successfully added"}


# ручка для обновления данных в Redis
@app.put("/write_data")
async def update_data(data: Data):
    if not redis_client.exists(data.phone):
        raise HTTPException(status_code=404, detail="Data not found")
    redis_client.set(data.phone, data.address)
    return {"message": "Successfully updated"}


# ручка для получения данных из Redis
@app.get("/check_data")
async def check_data(phone: str):
    address = redis_client.get(phone)
    if address is None:
        raise HTTPException(status_code=404, detail="Data not found")
    return {"phone": phone, "address": address}