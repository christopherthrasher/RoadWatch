from datetime import datetime

from pydantic import BaseModel, Field


class DetectionCreate(BaseModel):
    latitude: float = Field(ge=-90, le=90)
    longitude: float = Field(ge=-180, le=180)
    confidence: float
    timestamp: datetime