from fastapi import FastAPI

app = FastAPI()

@app.get("/")
async def welcome_msg():
    return {
        "message": "Welcome to FAST API"
    }