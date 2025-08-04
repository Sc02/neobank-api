from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class TransactionCreate(BaseModel):
    amount: float = Field(..., gt=0)
    type: str  # "deposit" or "withdrawal"
    category: Optional[str] = "general"

class TransactionResponse(BaseModel):
    id: int
    from_user: int | None
    to_user: int | None
    amount: float
    type: str
    category: str
    timestamp: datetime

    class Config:
        orm_mode = True
        json_encoders = {
            datetime: lambda v: v.isoformat(),  # 👈 Converts datetime to string
        }
