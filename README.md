# Campus Lost & Found API

A REST API built with FastAPI and SQLModel for managing lost and found items on a college campus.

## Features

- Create lost/found items
- Get all items
- Get a specific item by ID
- Update an item
- Delete an item
- Filter items by status
- Filter items by category
- SQLite database integration
- Input validation
- HTTP error handling

## Technologies Used

- Python
- FastAPI
- SQLModel
- SQLite
- Uvicorn

## API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| POST | `/items` | Create a new item |
| GET | `/items` | Get all items |
| GET | `/items/{item_id}` | Get item by ID |
| PUT | `/items/{item_id}` | Update an item |
| DELETE | `/items/{item_id}` | Delete an item |
| GET | `/items/status/{status}` | Filter by status |
| GET | `/items/category/{category}` | Filter by category |

## How to Run

Install dependencies:

```bash
pip install fastapi sqlmodel uvicorn
