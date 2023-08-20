from fastapi.testclient import TestClient
from main import app
from picture import app
from uitl_enums import AnalyseType

client = TestClient(app)

test_image = ["test/test_image.jpg", "test/test_image2.jpg"]


def test_yolo_upload():
    with open(test_image[1], "rb") as image_file:
        response = client.post(
        "/ai/yolo/analyse/", files={"file": (test_image[1], image_file)}, params={"type": AnalyseType.IMAGE})

    assert response.status_code == 200


def test_data_picture_upload():
    with open(test_image[0], "rb") as image_file:
        response = client.post(
            "/ai/data/upload/", files={"file": ("test_image.jpg", image_file)})

    assert response.status_code == 200
