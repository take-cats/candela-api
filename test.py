from fastapi.testclient import TestClient
from main import app
from picture import app

client = TestClient(app)

def test_picture_upload():
    with open("test_image.jpg", "rb") as image_file:
        response = client.post("/ai/upload/", files={"file": ("test_image.jpg", image_file)})

    assert response.status_code == 200

def test_data_picture_upload():
    with open("test_image.jpg", "rb") as image_file:
        response = client.post("/ai/data/upload/", files={"file": ("test_image.jpg", image_file)})

    assert response.status_code == 200