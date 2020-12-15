from typing import List, Optional

import redis
from fastapi import HTTPException, APIRouter, Depends, Query
from starlette.status import HTTP_404_NOT_FOUND
from sqlalchemy.orm import Session

from db.schemas import CreateVehicleSchema, VehicleSchema, CreateVehiclePositionSchema
from db.functions import (
    create_vehicle,
    get_vehicle_by_id,
    get_vehicles_by_plate_number,
    get_vehicles_by_ids,
)
from db.base import get_db

router = APIRouter()

redis_client = redis.Redis(host="redis", port=6379, db=0)


@router.post("", response_model=VehicleSchema)
def add_vehicles(vehicle: CreateVehicleSchema, db: Session = Depends(get_db)):
    new_vehicle = create_vehicle(db=db, vehicle=vehicle)
    return new_vehicle


@router.get("", response_model=Optional[List[VehicleSchema]])
def list_vehicles(
    plate_number: Optional[str] = Query(default=None), db: Session = Depends(get_db)
):
    vehicles = get_vehicles_by_plate_number(db=db, plate_number=plate_number)
    return vehicles


@router.get("/{vehicle_id}", response_model=VehicleSchema)
def get_vehicle(vehicle_id: int, db: Session = Depends(get_db)):
    vehicle = get_vehicle_by_id(db=db, vehicle_id=vehicle_id)
    if vehicle is None:
        raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail="Vehicle not found.")
    return vehicle


@router.post("/{vehicle_id}/position")
def add_vehicles(
    vehicle_id: int,
    vehicle_position: CreateVehiclePositionSchema,
    db: Session = Depends(get_db),
):
    vehicle = get_vehicle_by_id(db=db, vehicle_id=vehicle_id)
    if vehicle is None:
        raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail="Vehicle not found.")

    if redis_client.get(vehicle_id):
        redis_client.delete([vehicle_id])
    redis_client.geoadd(
        "vehicles", [vehicle_position.lng, vehicle_position.lat], vehicle_id
    )
    return {}


@router.get("", response_model=Optional[List[VehicleSchema]])
def get_vehicle_distance(
    nearby_radius: int = Query,
    Lng: float = Query,
    Lat: float = Query,
    db: Session = Depends(get_db),
):

    items = redis_client.georadius(
        name="vehicles", longitude=Lng, latitude=Lat, radius=nearby_radius
    )
    ids = [item for item in items]

    vehicles = get_vehicles_by_ids(db=db, ids=ids)
    return vehicles
