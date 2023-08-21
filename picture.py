import os
from fastapi import UploadFile
from main import app

@app.post("/ai/upload/")
def get_picture(file: UploadFile):
    """
    사진을 받아서 picture/finding 폴더에 넣습니다.

    :param file: 사진을 받아옵니다.
    """

    UPLOAD_FOLDER = "picture/finding"

    file_path = os.path.join(UPLOAD_FOLDER, file.filename)

    with open(file_path, "wb") as f:
        f.write(file.file.read())


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
