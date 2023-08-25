import os
import pytest

from main import app
from fastapi.testclient import TestClient

client = TestClient(app)


@pytest.fixture
def upload_file():
    return open("./test/assets/living_room.png", "rb")


@pytest.mark.asyncio
async def test_learn_data_upload(upload_file):
    response = await client.post("/data/upload/", files={"file": upload_file})
    assert response.status_code == 200
    assert os.path.exists("data/learning/living_room.png")
    os.remove("data/learning/living_room.png")
