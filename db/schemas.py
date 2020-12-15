from pydantic import BaseModel, Field


class CreateVehicleSchema(BaseModel):
    model: str
    full_name: str
    plate_number: str


class VehicleSchema(BaseModel):
    id: int
    model: str
    full_name: str
    plate_number: str

    class Config:
        orm_mode = True


class CreateVehiclePositionSchema(BaseModel):
    lng: float = Field(gte=-180, lte=180)
    lat: float = Field(gte=-90, lte=90)
