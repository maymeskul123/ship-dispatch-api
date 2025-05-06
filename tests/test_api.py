from fastapi.testclient import TestClient
from main import app
import time

client = TestClient(app)

def test_post_and_get_ship():
    ship_id = "ship123"
    t = int(time.time())

    # 1. Flush data
    response = client.post("/v1/api/flush")
    assert response.status_code == 200

    # 2. Send position
    res = client.post(f"/v1/api/ships/{ship_id}/position", json={"time": t, "x": 0, "y": 0})
    assert res.status_code == 201
    assert res.json()["status"] == "green"

    # 3. Get ship record
    res = client.get(f"/v1/api/ships/{ship_id}")
    assert res.status_code == 200
    assert res.json()["id"] == ship_id
    assert len(res.json()["positions"]) == 1

    # 4. Get all ships
    res = client.get("/v1/api/ships")
    assert res.status_code == 200
    assert ship_id in str(res.json())
