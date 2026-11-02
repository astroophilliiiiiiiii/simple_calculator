# -*- coding: utf-8 -*-
from fastapi import FastAPI
from pydantic import BaseModel, validator

app = FastAPI()


class InventoryItemCreate(BaseModel):
    name: str
    quantity: int

    @validator('name')
    def name_must_not_be_empty(cls, v):
        if not v or not v.strip():
            raise ValueError('name must not be empty')
        return v

    @validator('quantity')
    def quantity_must_be_non_negative(cls, v):
        if v < 0:
            raise ValueError('quantity must be non-negative')
        return v


@app.post('/items/', status_code=201)
def create_item(item: InventoryItemCreate):
    # In a real application you would persist the item to a database.
    # For this simple example we just echo the validated data back.
    return item
