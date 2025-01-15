from pydantic import BaseModel
from typing import List

class Vuelo(BaseModel):
    OPERA: str
    TIPOVUELO: str
    MES: int

class SolicitudVuelos(BaseModel):
    flights: List[Vuelo]