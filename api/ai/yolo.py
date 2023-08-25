import os
import shutil
from typing import BinaryIO
from fastapi.responses import FileResponse, StreamingResponse

import torch
from fastapi import UploadFile, APIRouter, HTTPException

from etc.enums import AnalyseType

router = APIRouter()

model = torch.hub.load("ultralytics/yolov5", "yolov5s")


async def _analyser(file: UploadFile, a_type: AnalyseType):
    _TEMP_IMAGE = "data/analyse"

    # if "exp*" folder already exists remove all folders
    for folder in os.listdir(os.path.abspath("./runs/detect")):
        if folder.startswith("exp"):
            shutil.rmtree(os.path.abspath(f"./runs/detect/{folder}"))

    # save image to temp folder
    full_path = os.path.abspath(os.path.join(_TEMP_IMAGE, str(file.filename)))
    if os.name == "nt":
        full_path = full_path.replace("\\", "/")

    # if file already exists
    if os.path.exists(full_path):
        raise HTTPException(
            status_code=400, detail="That image is already requested.")
    else:
        os.makedirs(os.path.dirname(full_path), exist_ok=True)

        with open(full_path, "wb") as buf:
            shutil.copyfileobj(file.file, buf)

    # analyse and remove temp image
    analyzed = model(full_path)
    os.remove(full_path)

    if a_type == AnalyseType.TEXT:
        res = analyzed.pandas().xyxy[0].values.tolist()
        items = [item[6] for item in res]

        counted = {}

        for item in items:
            if item in counted:
                counted[item] += 1
            else:
                counted[item] = 1

        return counted
    elif a_type == AnalyseType.IMAGE:
        _RESULT_EXT = ".result"

        analyzed.save()

        full_path = os.path.abspath(
            os.path.join(_TEMP_IMAGE, file.filename.split('.')[0]))

        shutil.move(
            os.path.join(os.path.abspath(
                f"./runs/detect/exp/{file.filename.split('.')[0]}") + ".jpg"),
            full_path + _RESULT_EXT + ".jpg"
        )

        result_byte = open(full_path + _RESULT_EXT + ".jpg", "rb")

        result = result_byte.read()
        result_byte.close()

        return FileResponse(
            full_path + _RESULT_EXT + ".jpg",
            media_type="image/jpg",
            filename=file.filename.split('.')[0] + _RESULT_EXT + ".jpg"
        )


@router.post(
    "/analyse",
    summary="Analyse image with YoLo",
    description="Analyse image with YoLo",
    response_description="Type 0: Return result strings, Type 1: Return image with bounding crops",
)
async def analyse_image(file: UploadFile, a_type: AnalyseType):
    # if isn't image
    content_type = file.content_type

    if content_type != None and content_type.split("/")[0] != "image":
        raise HTTPException(status_code=400, detail="File is not image")

    return await _analyser(file, a_type)
