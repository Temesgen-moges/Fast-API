from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional
from fastapi.middleware.cors import CORSMiddleware

# Pydantic model for an Item
class Item(BaseModel):
    name: str
    price: float
    is_offer: Optional[bool] = False   # optional field, default False

class ItemNameOnly(BaseModel):
    name: str

app = FastAPI()

# Fake database (a simple Python list)
fake_items_db = [
    {"id": 1, "name": "Apple", "price": 0.99},
    {"id": 2, "name": "Banana", "price": 0.59},
    {"id": 3, "name": "Orange", "price": 0.79},
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],   # Allow all origins (for development only)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
) 


@app.get("/items/{item_id}")
def get_item(item_id: int):
    # Search for the item with the given id
    for item in fake_items_db:
        if item["id"] == item_id:
            return item
    # If not found, return a custom message (error handling later)
    return {"error": "Item not found"}

@app.get("/items/")
def list_items(skip: int = 0, limit: int = 10, sort_by: str = "name"):
    """
    Returns a slice of the items.
    - skip: how many items to skip from the start
    - limit: maximum number of items to return
    - sort_by: field to sort by ('name' or 'price')
    """
    # Sort the list based on sort_by
    if sort_by == "price":
        sorted_list = sorted(fake_items_db, key=lambda x: x["price"])
    else:  # default sort by name
        sorted_list = sorted(fake_items_db, key=lambda x: x["name"])
    # Apply skip and limit
    return sorted_list[skip : skip + limit]

@app.get("/items/names/", response_model=list[ItemNameOnly])
def get_all_names():
    return fake_items_db   # FastAPI will filter each item to only 'name'


@app.post("/items/")
def create_item(new_item: Item):
    # Generate a new id (max existing id + 1)
    new_id = max((item["id"] for item in fake_items_db), default=0) + 1
    item_dict = new_item.dict()
    item_dict["id"] = new_id
    fake_items_db.append(item_dict)
    return {"message": "Item created", "item": item_dict}


















# from fastapi import FastAPI

# # Create the FastAPI app
# app = FastAPI()


# # Home route
# @app.get("/")
# async def root():
#     return {"message": "Hello World"}


# # About route
# @app.get("/about")
# async def about():
#     return {
#         "name": "Temesgen",
#         "role": "Backend Developer",
#         "language": "Python"
#     }


# # Dynamic route
# @app.get("/user/{user_id}")
# async def get_user(user_id: int):
#     return {
#         "user_id": user_id,
#         "status": "User found"
#     }