---
name: fastapi-crud-operations
description: Generates complete CRUD endpoints for FastAPI with proper error handling, status codes, and SQLModel integration. Use when creating, reading, updating, or deleting resources through FastAPI routes.
---

# FastAPI CRUD Operations

Generate complete CRUD endpoints following FastAPI best practices.

## Core Principles

- Use proper HTTP methods (GET, POST, PUT, DELETE)
- Include status codes (201 for create, 404 for not found)
- Always use HTTPException for errors
- Include Session dependency injection
- Add docstrings to all endpoints

## Basic CRUD Pattern

```python
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select
from datetime import datetime

router = APIRouter()

# CREATE - POST with 201 status
@router.post("/", status_code=status.HTTP_201_CREATED)
def create_item(item: ItemCreate, session: Session = Depends(get_session)):
    """Create a new item."""
    db_item = Item.model_validate(item)
    session.add(db_item)
    session.commit()
    session.refresh(db_item)
    return db_item

# READ ALL - GET with pagination support
@router.get("/", response_model=List[ItemRead])
def read_items(session: Session = Depends(get_session), offset: int = 0, limit: int = 100):
    """Get all items with optional pagination."""
    items = session.exec(select(Item).offset(offset).limit(limit)).all()
    return items

# READ ONE - GET with 404 handling
@router.get("/{item_id}", response_model=ItemRead)
def read_item(item_id: int, session: Session = Depends(get_session)):
    """Get a specific item by ID."""
    item = session.get(Item, item_id)
    if not item:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not found")
    return item

# UPDATE - PUT with 404 handling
@router.patch("/{item_id}", response_model=ItemRead)
def update_item(item_id: int, item: ItemUpdate, session: Session = Depends(get_session)):
    """Update an existing item."""
    db_item = session.get(Item, item_id)
    if not db_item:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not found")
    item_data = item.model_dump(exclude_unset=True)
    for key, value in item_data.items():
        setattr(db_item, key, value)
    session.add(db_item)
    session.commit()
    session.refresh(db_item)
    return db_item

# DELETE - DELETE with 404 handling
@router.delete("/{item_id}")
def delete_item(item_id: int, session: Session = Depends(get_session)):
    """Delete an item."""
    item = session.get(Item, item_id)
    if not item:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not found")
    session.delete(item)
    session.commit()
    return {"ok": True}
```

## Best Practices

1. **Separate models**: Use `ItemCreate`, `ItemRead`, `ItemUpdate` models separate from database `Item` model
2. **Proper status codes**: 201 for creation, 404 for missing resources, 422 for validation errors
3. **HTTPException**: Always raise HTTPException with descriptive messages
4. **Session management**: Use dependency injection for database sessions
5. **PATCH vs PUT**: Prefer PATCH for partial updates using `exclude_unset=True`
