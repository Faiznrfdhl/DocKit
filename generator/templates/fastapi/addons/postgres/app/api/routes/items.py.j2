from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models.item import Item
from app.schemas.item import ItemCreate, ItemOut

router = APIRouter(tags=["Items"])


@router.get("/items", response_model=list[ItemOut])
def list_items(db: Session = Depends(get_db)):
    return db.query(Item).all()


@router.post("/items", response_model=ItemOut, status_code=201)
def create_item(payload: ItemCreate, db: Session = Depends(get_db)):
    item = Item(**payload.model_dump())
    db.add(item)
    db.commit()
    db.refresh(item)
    return item


@router.get("/items/{item_id}", response_model=ItemOut)
def get_item(item_id: int, db: Session = Depends(get_db)):
    item = db.get(Item, item_id)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    return item
