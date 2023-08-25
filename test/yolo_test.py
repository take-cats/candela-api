from pytest import fixture
from fastapi.testclient import TestClient
from os import path
from PIL import Image
from io import BytesIO

from main import app
from etc.enums import AnalyseType


client = TestClient(app)


@fixture(scope="module")
def test_img():
    # 이미지 파일 경로
    image_path = path.join(
        path.dirname(__file__),
        "assets", "living_room.png"
    )
    with open(image_path, "rb") as f:
        image_bytes = f.read()
    return image_bytes


def test_yolo_text(test_img):
    res = client.post(
        f"/ai/yolo/analyse?a_type={AnalyseType.TEXT}",
        files={"file": (
            "test.png",
            BytesIO(test_img),
            "image/png"
        )},
    )
    assert res.status_code == 200
    assert res.json() == {
        "couch": 1,
        "dining table": 2,
        "vase": 1,
        "chair": 5,
        "refrigerator": 1,
        "sink": 1,
        "potted plant": 1,
        "tv": 1
    }


def test_yolo_image(test_img):
    res = client.post(
        f"/ai/yolo/analyse?a_type={AnalyseType.IMAGE}",
        files={"file": (
            "test.png",
            BytesIO(test_img),
            "image/png"
        )},
    )
    assert res.status_code == 200
