from enum import Enum

from fastapi import FastAPI, HTTPException, status
from sqlmodel import Field, SQLModel, Session, create_engine, select


# -----------------------------
# FastAPI application
# -----------------------------

app = FastAPI(
    title="Campus Lost & Found API",
    description="REST API for managing lost and found items on campus",
    version="1.0.0"
)


# -----------------------------
# Status Enum
# -----------------------------

class ItemStatus(str, Enum):
    Lost = "Lost"
    Found = "Found"
    Returned = "Returned"


# -----------------------------
# Item Database Model
# -----------------------------

class Item(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)

    title: str
    description: str
    category: str
    location: str
    reported_by: str
    status: ItemStatus


# -----------------------------
# SQLite Database
# -----------------------------

sqlite_url = "sqlite:///lost_found.db"

engine = create_engine(
    sqlite_url,
    echo=True
)


# -----------------------------
# Create database table
# -----------------------------

@app.on_event("startup")
def on_startup():
    SQLModel.metadata.create_all(engine)


# -----------------------------
# POST /items
# Create new item
# -----------------------------

@app.post(
    "/items",
    response_model=Item,
    status_code=status.HTTP_201_CREATED
)
def create_item(item: Item):

    # Validate title
    if not item.title.strip():
        raise HTTPException(
            status_code=400,
            detail="Title must not be empty"
        )

    # Validate description
    if len(item.description.strip()) < 5:
        raise HTTPException(
            status_code=400,
            detail="Description must contain meaningful text"
        )

    with Session(engine) as session:
        session.add(item)
        session.commit()
        session.refresh(item)

        return item


# -----------------------------
# GET /items
# Get all items
# -----------------------------

@app.get("/items", response_model=list[Item])
def get_items():

    with Session(engine) as session:
        items = session.exec(
            select(Item)
        ).all()

        return items


# -----------------------------
# GET /items/{item_id}
# Get specific item
# -----------------------------

@app.get("/items/{item_id}", response_model=Item)
def get_item(item_id: int):

    with Session(engine) as session:

        item = session.get(Item, item_id)

        if not item:
            raise HTTPException(
                status_code=404,
                detail="Item not found"
            )

        return item


# -----------------------------
# PUT /items/{item_id}
# Update item
# -----------------------------

@app.put("/items/{item_id}", response_model=Item)
def update_item(item_id: int, updated_item: Item):

    with Session(engine) as session:

        existing_item = session.get(Item, item_id)

        if not existing_item:
            raise HTTPException(
                status_code=404,
                detail="Item not found"
            )

        # Validation
        if not updated_item.title.strip():
            raise HTTPException(
                status_code=400,
                detail="Title must not be empty"
            )

        if len(updated_item.description.strip()) < 5:
            raise HTTPException(
                status_code=400,
                detail="Description must contain meaningful text"
            )

        existing_item.title = updated_item.title
        existing_item.description = updated_item.description
        existing_item.category = updated_item.category
        existing_item.location = updated_item.location
        existing_item.reported_by = updated_item.reported_by
        existing_item.status = updated_item.status

        session.add(existing_item)
        session.commit()
        session.refresh(existing_item)

        return existing_item


# -----------------------------
# DELETE /items/{item_id}
# Delete item
# -----------------------------

@app.delete("/items/{item_id}")
def delete_item(item_id: int):

    with Session(engine) as session:

        item = session.get(Item, item_id)

        if not item:
            raise HTTPException(
                status_code=404,
                detail="Item not found"
            )

        session.delete(item)
        session.commit()

        return {
            "message": "Item deleted successfully"
        }


# -----------------------------
# GET /items/status/{status}
# Filter by status
# -----------------------------

@app.get("/items/status/{status}", response_model=list[Item])
def get_items_by_status(status: ItemStatus):

    with Session(engine) as session:

        items = session.exec(
            select(Item).where(Item.status == status)
        ).all()

        return items


# -----------------------------
# GET /items/category/{category}
# Filter by category
# -----------------------------

@app.get("/items/category/{category}", response_model=list[Item])
def get_items_by_category(category: str):

    with Session(engine) as session:

        items = session.exec(
            select(Item).where(Item.category == category)
        ).all()

        return items