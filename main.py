import os
from fastapi import APIRouter, FastAPI
import routers.ai as ai

# app = FastAPI(root_path="/api/v1")  # https://fastapi.tiangolo.com/advanced/behind-a-proxy/
app = FastAPI()

app.include_router(ai.router, prefix="/ai", tags=["ai"])


@app.get("/")
def root():
    return {"status": 200}


if __name__ == "__main__":
    os.system("python -m uvicorn main:app")
