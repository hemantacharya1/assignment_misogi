from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class TicketCreate(BaseModel):
    title: str
    description: str

class TicketOut(BaseModel):
    id: int
    title: str
    description: str
    auto_category: Optional[str]
    tags: Optional[str]
    priority: Optional[str]
    generated_response: Optional[str]
    confidence_score: Optional[float]
    status: str
    created_at: datetime

    class Config:
        orm_mode = True
