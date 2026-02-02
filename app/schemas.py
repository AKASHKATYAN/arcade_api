from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime

# --- CARD SCHEMAS ---
class CardBase(BaseModel):
    card_id: str = Field(..., min_length=10, max_length=10)
    owner_name: str
    contact_no: str = Field(..., min_length=10, max_length=10)

class CardCreate(CardBase):
    pass

class CardResponse(CardBase):
    balance: float
    arcade_id: str

    class Config:
        from_attributes = True

# --- TRANSACTION SCHEMAS ---
class RechargeRequest(BaseModel):
    card_id: str
    amount: float = Field(..., gt=0) # Must be greater than 0

class PunchRequest(BaseModel):
    card_id: str
    machine_id: str

# --- USER & AUTH SCHEMAS ---
class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None
    role: Optional[str] = None
    arcade_id: Optional[str] = None

class RefundRequest(BaseModel):
    card_id: str
    reason: Optional[str] = "Customer request"    