import os
from fastapi import UploadFile
from main import app
from uitl_enums import AnalyseType
from yolo.yolo import YoLo


@app.post("/ai/yolo/analyse/")
def get_picture(file: UploadFile, type: AnalyseType):
    """
    사진을 받아서 yolo 함수를 통해서 사진을 분석합니다.

    :param file: 사진을 받아옵니다.
    """
    YoLo.analyser(file.filename, type)

    return {"status": 200}


@app.post("/ai/data/upload/")
def get_picture(file: UploadFile):
    """
    사진을 받아서 picture/leaning 폴더에 넣습니다.

    :param file: 사진을 받아옵니다.
    """

    UPLOAD_FOLDER = "picture/learning"

    file_path = os.path.join(UPLOAD_FOLDER, file.filename)

    with open(file_path, "wb") as f:
        f.write(file.file.read())

    return {"status": 200}
