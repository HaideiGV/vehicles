from fastapi import FastAPI

from api import vehicles
from db.base import Base, engine

Base.metadata.create_all(bind=engine)


app = FastAPI()


app.include_router(vehicles.router, prefix="/vehicles")
