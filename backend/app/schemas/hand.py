from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime


class PokerHandCreate(BaseModel):
    stacks: List[int] = Field(..., description="Starting stacks for 6 players")
    dealer_index: int = Field(0, description="Dealer position (0-5)")
    small_blind_index: int = Field(1, description="Small blind position (0-5)")
    big_blind_index: int = Field(2, description="Big blind position (0-5)")
    actions: List[str] = Field(default_factory=list, description="Action sequence")
    hole_cards: List[str] = Field(default_factory=list, description="Hole cards for each player")
    board: str = Field("", description="Board cards")


class PokerHandResponse(BaseModel):
    id: str
    stacks: List[int]
    dealer_index: int
    small_blind_index: int
    big_blind_index: int
    actions: List[str]
    hole_cards: List[str]
    board: str
    winnings: List[int]
    created_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True


class PokerHandUpdate(BaseModel):
    actions: Optional[List[str]] = None
    hole_cards: Optional[List[str]] = None
    board: Optional[str] = None