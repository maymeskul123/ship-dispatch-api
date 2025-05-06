from fastapi import FastAPI, HTTPException, Path
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
from typing import Dict, List, Optional
import time as systime
import math

app = FastAPI()

# In-memory storage
ships_db: Dict[str, List[Dict]] = {}

class Position(BaseModel):
    x: int
    y: int

class PositionRequest(BaseModel):
    time: int
    x: int
    y: int

class PositionResponse(BaseModel):
    time: int
    x: int
    y: int
    speed: float
    status: str  # green | yellow | red

class ShipStatus(BaseModel):
    id: str
    last_time: int
    last_status: str
    last_speed: float
    last_position: Position

class ShipRecord(BaseModel):
    id: str
    positions: List[Dict]

@app.post("/v1/api/ships/{ship_id}/position", response_model=PositionResponse, status_code=201)
def update_position(ship_id: str, pos: PositionRequest):
    current_unix = int(systime.time())

    if pos.time > current_unix:
        raise HTTPException(status_code=422, detail="time out of range")

    new_entry = {
        "time": pos.time,
        "position": {"x": pos.x, "y": pos.y},
    }

    history = ships_db.setdefault(ship_id, [])

    if history:
        last = history[-1]
        if pos.time <= last["time"]:
            raise HTTPException(status_code=422, detail="time out of range")

        dt = pos.time - last["time"]
        dx = pos.x - last["position"]["x"]
        dy = pos.y - last["position"]["y"]
        speed = math.sqrt(dx ** 2 + dy ** 2) / dt
    else:
        speed = 0.0

    new_entry["speed"] = speed
    new_entry["status"] = get_status(ship_id, pos.time, pos.x, pos.y, speed)

    history.append(new_entry)

    return PositionResponse(
        time=pos.time,
        x=pos.x,
        y=pos.y,
        speed=speed,
        status=new_entry["status"]
    )

@app.get("/v1/api/ships", response_model=Dict[str, List[ShipStatus]])
def get_all_ships():
    result = []
    for ship_id, positions in ships_db.items():
        if positions:
            last = positions[-1]
            result.append(ShipStatus(
                id=ship_id,
                last_time=last["time"],
                last_status=last["status"],
                last_speed=last.get("speed", 0.0),
                last_position=Position(x=last["position"]["x"], y=last["position"]["y"])
            ))
    return {"ships": result}

@app.get("/v1/api/ships/{ship_id}", response_model=ShipRecord)
def get_ship_records(ship_id: str = Path(...)):
    history = ships_db.get(ship_id)
    if history is None:
        raise HTTPException(status_code=404, detail="Ship not found")
    return {"id": ship_id, "positions": history}

@app.post("/v1/api/flush")
def flush():
    ships_db.clear()
    return JSONResponse(content={"message": "All data cleared."})

def get_status(current_id, now, x, y, speed):
    for other_id, records in ships_db.items():
        if other_id == current_id:
            continue

        if not records:
            continue

        last = records[-1]
        dt = now - last["time"]
        if dt > 60 or "speed" not in last:
            continue

        ox = last["position"]["x"]
        oy = last["position"]["y"]
        ospeed = last.get("speed", 0.0)
        dx = x - ox
        dy = y - oy

        if math.sqrt(dx ** 2 + dy ** 2) <= 1:
            return "red"
        elif math.sqrt(dx ** 2 + dy ** 2) <= 2:
            return "yellow"
    return "green"

# Basic test client for pytest
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8080, reload=True)
