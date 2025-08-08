from typing import List, Optional
from app.models.hand import PokerHand
from app.core.db import DatabaseManager


class HandRepository:
    def __init__(self, db_manager: DatabaseManager):
        self.db_manager = db_manager
    
    def save(self, hand: PokerHand) -> PokerHand:
        """Save a poker hand to database"""
        with self.db_manager.get_cursor() as cursor:
            cursor.execute("""
                INSERT INTO hands (
                    id, stacks, dealer_index, small_blind_index, big_blind_index,
                    actions, hole_cards, board, winnings
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                ON CONFLICT (id) DO UPDATE SET
                    stacks = EXCLUDED.stacks,
                    dealer_index = EXCLUDED.dealer_index,
                    small_blind_index = EXCLUDED.small_blind_index,
                    big_blind_index = EXCLUDED.big_blind_index,
                    actions = EXCLUDED.actions,
                    hole_cards = EXCLUDED.hole_cards,
                    board = EXCLUDED.board,
                    winnings = EXCLUDED.winnings
                RETURNING created_at
            """, (
                hand.id,
                hand.stacks,
                hand.dealer_index,
                hand.small_blind_index,
                hand.big_blind_index,
                hand.actions,
                hand.hole_cards,
                hand.board,
                hand.winnings
            ))
            
            result = cursor.fetchone()
            hand.created_at = result['created_at']
            return hand
    
    def get_all(self) -> List[PokerHand]:
        """Get all poker hands from database"""
        with self.db_manager.get_cursor() as cursor:
            cursor.execute("""
                SELECT id, stacks, dealer_index, small_blind_index, big_blind_index,
                       actions, hole_cards, board, winnings, created_at
                FROM hands 
                ORDER BY created_at DESC
            """)
            
            rows = cursor.fetchall()
            return [
                PokerHand(
                    id=row['id'],
                    stacks=list(row['stacks']),
                    dealer_index=row['dealer_index'],
                    small_blind_index=row['small_blind_index'],
                    big_blind_index=row['big_blind_index'],
                    actions=list(row['actions']),
                    hole_cards=list(row['hole_cards']),
                    board=row['board'],
                    winnings=list(row['winnings']),
                    created_at=row['created_at']
                )
                for row in rows
            ]
    
    def get_by_id(self, hand_id: str) -> Optional[PokerHand]:
        """Get a specific poker hand by ID"""
        with self.db_manager.get_cursor() as cursor:
            cursor.execute("""
                SELECT id, stacks, dealer_index, small_blind_index, big_blind_index,
                       actions, hole_cards, board, winnings, created_at
                FROM hands 
                WHERE id = %s
            """, (hand_id,))
            
            row = cursor.fetchone()
            if not row:
                return None
                
            return PokerHand(
                id=row['id'],
                stacks=list(row['stacks']),
                dealer_index=row['dealer_index'],
                small_blind_index=row['small_blind_index'],
                big_blind_index=row['big_blind_index'],
                actions=list(row['actions']),
                hole_cards=list(row['hole_cards']),
                board=row['board'],
                winnings=list(row['winnings']),
                created_at=row['created_at']
            )