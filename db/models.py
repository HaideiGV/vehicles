from sqlalchemy import Column, Integer, String

from .base import Base


class Vehicle(Base):
    __tablename__ = "vehicles"

    id = Column(Integer, primary_key=True, index=True)
    model = Column(String)
    full_name = Column(String)
    plate_number = Column(String)
