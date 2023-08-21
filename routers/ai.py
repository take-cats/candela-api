import os
import torch
from fastapi import UploadFile, APIRouter
from etc.enums import AnalyseType


router = APIRouter()


model = torch.hub.load("ultralytics/yolov5", "yolov5s")


async def _analyser(file: str, type: AnalyseType):
    if type == AnalyseType.IMAGE:
        return model(file).crop()
    elif type == AnalyseType.TEXT:
        res = model(file).pandas().xyxy[0].values.tolist()
        object: list[str] = [i[6] for i in res]  # Set of labels
        return {i: object.count(i) for i in object}


@router.post(
    "/yolo/analyse/",
    summary="Analyse image with YoLo",
    response_description="Type 0: Return result strings, Type 1: Return image with bounding boxes",
)
async def analyse_image(file: UploadFile, type: AnalyseType):
    _analyser(file.filename, type)


@router.post(
    "/data/upload/",
    summary="Upload learning data",
)
async def learn_data_upload(file: UploadFile):
    _UPLOAD_DIR = "data/learning"

    file_path = os.path.join(_UPLOAD_DIR, file.filename)

    with open(file_path, "wb") as f:
        f.write(file.file.read())
