from fastapi import FastAPI
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

app = FastAPI(
    title="Simple FastAPI App",
    description="簡単なFastAPIアプリケーション",
    version="1.0.0"
)


# データモデル
class Item(BaseModel):
    id: Optional[int] = None
    name: str
    description: Optional[str] = None
    price: float


class ItemCreate(BaseModel):
    name: str
    description: Optional[str] = None
    price: float


# インメモリデータストア
items_db = []
next_id = 1


@app.get("/")
async def root():
    """ルートエンドポイント"""
    return {
        "message": "FastAPIアプリへようこそ！",
        "endpoints": {
            "health": "/health",
            "items": "/items",
            "docs": "/docs"
        }
    }


@app.get("/health")
async def health_check():
    """ヘルスチェックエンドポイント"""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat()
    }


@app.get("/items", response_model=List[Item])
async def get_items():
    """すべてのアイテムを取得"""
    return items_db


@app.get("/items/{item_id}", response_model=Item)
async def get_item(item_id: int):
    """IDでアイテムを取得"""
    item = next((item for item in items_db if item["id"] == item_id), None)
    if item is None:
        return JSONResponse(
            status_code=404,
            content={"detail": f"Item {item_id} not found"}
        )
    return item


@app.post("/items", response_model=Item, status_code=201)
async def create_item(item: ItemCreate):
    """新しいアイテムを作成"""
    global next_id
    new_item = {
        "id": next_id,
        "name": item.name,
        "description": item.description,
        "price": item.price
    }
    items_db.append(new_item)
    next_id += 1
    return new_item


@app.put("/items/{item_id}", response_model=Item)
async def update_item(item_id: int, item: ItemCreate):
    """アイテムを更新"""
    item_index = next(
        (i for i, item_data in enumerate(items_db) if item_data["id"] == item_id),
        None
    )
    if item_index is None:
        return JSONResponse(
            status_code=404,
            content={"detail": f"Item {item_id} not found"}
        )
    
    updated_item = {
        "id": item_id,
        "name": item.name,
        "description": item.description,
        "price": item.price
    }
    items_db[item_index] = updated_item
    return updated_item


@app.delete("/items/{item_id}", status_code=204)
async def delete_item(item_id: int):
    """アイテムを削除"""
    item_index = next(
        (i for i, item_data in enumerate(items_db) if item_data["id"] == item_id),
        None
    )
    if item_index is None:
        return JSONResponse(
            status_code=404,
            content={"detail": f"Item {item_id} not found"}
        )
    items_db.pop(item_index)
    return None

