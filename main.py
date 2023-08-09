import os
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def root():
    return {"status" : 200}

if __name__ == "__main__":
    os.system("python -m uvicorn main:app")