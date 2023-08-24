import os
import shutil

import torch
from fastapi import UploadFile, APIRouter, HTTPException

from etc.enums import AnalyseType

router = APIRouter()

model = torch.hub.load("ultralytics/yolov5", "yolov5s")


async def _analyser(file: UploadFile, a_type: AnalyseType):
    _TEMP_IMAGE = "data/analyse"

    full_path = os.path.abspath(os.path.join(_TEMP_IMAGE, file.filename))
    if os.name == "nt":
        full_path = full_path.replace("\\", "/")

    # if file already exists
    if os.path.exists(full_path):
        raise HTTPException(status_code=400, detail="That image is already requested.")
    else:
        os.makedirs(os.path.dirname(full_path), exist_ok=True)

        with open(full_path, "wb") as buf:
            shutil.copyfileobj(file.file, buf)

    analyzed = model(full_path)
    os.remove(full_path)

    if a_type == AnalyseType.TEXT:
        res = analyzed.pandas().xyxy[0].values.tolist()
        return res
    elif a_type == AnalyseType.IMAGE:
        return model(file).render()


@router.post(
    "/analyse",
    summary="Analyse image with YoLo",
    description="Analyse image with YoLo",
    response_description="Type 0: Return result strings, Type 1: Return image with bounding crops",
)
async def analyse_image(file: UploadFile, a_type: AnalyseType):
    # if isn't image
    if file.content_type.split("/")[0] != "image":
        raise HTTPException(status_code=400, detail="File is not image")

    await _analyser(file, a_type)
