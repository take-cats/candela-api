import uvicorn
from fastapi import FastAPI

from api.ai import clas, yolo

app = FastAPI()

app.include_router(yolo.router, prefix="/ai/yolo", tags=["ai"])
app.include_router(clas.router, prefix="/ai/clas", tags=["ai"])


@app.get("/")
def root():
    return {"message": "Welcome to Candela API!"}


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
