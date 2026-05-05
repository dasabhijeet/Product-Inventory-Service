from fastapi import FastAPI, HTTPException
from fastapi.concurrency import run_in_threadpool
from utils.mysql_utils import init_db
import utils.mysql_utils as db

app = FastAPI()
init_db()

# Product

@app.post("/products")
async def create_product(payload: dict):
    try:
        return await run_in_threadpool(db.create_product, payload)
    except Exception as e:
        raise HTTPException(400, str(e))

@app.get("/products")
async def get_products(limit: int = 10, offset: int = 0, search: str = None):
    return await run_in_threadpool(db.get_products, limit, offset, search)

@app.get("/products/{pid}")
async def get_product(pid: int):
    data = await run_in_threadpool(db.get_product, pid)
    if not data:
        raise HTTPException(404, "Product not found")
    return data

@app.put("/products/{pid}")
async def update_product(pid: int, payload: dict):
    try:
        return await run_in_threadpool(db.update_product, pid, payload)
    except Exception as e:
        raise HTTPException(400, str(e))

@app.delete("/products/{pid}")
async def delete_product(pid: int):
    return await run_in_threadpool(db.delete_product, pid)

# Inventory

@app.post("/inventory/add")
async def add_stock(payload: dict):
    try:
        return await run_in_threadpool(db.add_stock, payload)
    except Exception as e:
        raise HTTPException(400, str(e))


@app.post("/inventory/remove")
async def remove_stock(payload: dict):
    try:
        return await run_in_threadpool(db.remove_stock, payload)
    except Exception as e:
        raise HTTPException(400, str(e))