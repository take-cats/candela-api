import os

from fastapi import FastAPI

import api.ai.clas as clas
import api.ai.yolo as yolo

# app = FastAPI(root_path="/api/v1")  # https://fastapi.tiangolo.com/advanced/behind-a-proxy/
app = FastAPI()

app.include_router(yolo.router, prefix="/ai/yolo", tags=["ai"])
app.include_router(clas.router, prefix="/ai/clas", tags=["ai"])


@app.get("/")
def root():
    return


if __name__ == "__main__":
    os.system("python -m uvicorn main:app")
