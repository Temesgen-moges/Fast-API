from fastapi import FastAPI

# Create the FastAPI app
app = FastAPI()


# Home route
@app.get("/")
async def root():
    return {"message": "Hello World"}


# About route
@app.get("/about")
async def about():
    return {
        "name": "Temesgen",
        "role": "Backend Developer",
        "language": "Python"
    }


# Dynamic route
@app.get("/user/{user_id}")
async def get_user(user_id: int):
    return {
        "user_id": user_id,
        "status": "User found"
    }