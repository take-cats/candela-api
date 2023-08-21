from fastapi.testclient import TestClient
from main import app
from etc.enums import AnalyseType
from os import listdir

client = TestClient(app)

# ============== Test Data ============== #
_UPLOAD_DIR = "data/learning"

_ASSET_DIR = "test/assets"
_ASSET_IMAGES = [file for file in listdir(_ASSET_DIR) if file.endswith(".png")]


def _get_asset(name: str):
    if name not in _ASSET_IMAGES:
        raise Exception(
            "Cannot found test image. Please check test/assets directory.")
    else:
        return _ASSET_DIR + "/" + name
# ======================================= #


def test_analyse_yolo():
    image = open(_get_asset("living_room.png"), "rb")

    response = client.post(
        "/ai/yolo/analyse/",
        files={"file": ("living_room.png", image)},
        params={"type": AnalyseType.IMAGE}
    )

    assert response.status_code == 200


def test_training_data_upload():
    with open(_ASSET_IMAGES[0], "rb") as image_file:
        response = client.post(
            "/ai/data/upload/", files={"file": ("test_image.jpg", image_file)})

    assert response.status_code == 200
