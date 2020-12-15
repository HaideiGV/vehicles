from typing import List

from sqlalchemy.orm import Session

from . import models, schemas


def create_vehicle(db: Session, vehicle: schemas.CreateVehicleSchema):
    new_vehicle = models.Vehicle(
        model=vehicle.model,
        full_name=vehicle.full_name,
        plate_number=vehicle.plate_number,
    )
    db.add(new_vehicle)
    db.commit()
    return new_vehicle


def get_vehicle_by_id(db: Session, vehicle_id: int):
    return db.query(models.Vehicle).filter(models.Vehicle.id == vehicle_id).first()


def get_vehicles_by_plate_number(db: Session, plate_number: str):
    return (
        db.query(models.Vehicle)
        .filter(models.Vehicle.plate_number == plate_number)
        .all()
    )


def get_vehicles_by_ids(db: Session, ids: List[int]):
    return db.query(models.Vehicle).filter(models.Vehicle.id.in_(ids)).all()
