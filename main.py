import os
from fastapi import APIRouter, FastAPI

app = FastAPI()

app.include_router(APIRouter(prefix="/api"))


@app.get("/")
def root():
    return {"status": 200}


if __name__ == "__main__":
    os.system("python -m uvicorn main:app")
