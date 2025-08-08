from dataclasses import dataclass, field
from typing import List, Optional
from datetime import datetime
import uuid


@dataclass
class PokerHand:
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    stacks: List[int] = field(default_factory=list)
    dealer_index: int = 0
    small_blind_index: int = 1
    big_blind_index: int = 2
    actions: List[str] = field(default_factory=list)
    hole_cards: List[str] = field(default_factory=list)  # 6 players * 2 cards each
    board: str = ""
    winnings: List[int] = field(default_factory=list)
    created_at: Optional[datetime] = None
    
    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "stacks": self.stacks,
            "dealer_index": self.dealer_index,
            "small_blind_index": self.small_blind_index,
            "big_blind_index": self.big_blind_index,
            "actions": self.actions,
            "hole_cards": self.hole_cards,
            "board": self.board,
            "winnings": self.winnings,
            "created_at": self.created_at.isoformat() if self.created_at else None
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> 'PokerHand':
        hand = cls(**{k: v for k, v in data.items() if k != 'created_at'})
        if data.get('created_at'):
            hand.created_at = datetime.fromisoformat(data['created_at']) if isinstance(data['created_at'], str) else data['created_at']
        return hand