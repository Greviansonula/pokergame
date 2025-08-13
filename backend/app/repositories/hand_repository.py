from typing import List, Optional
from app.models.hand import PokerHand
from app.core.db import DatabaseManager
import logging

# Configure logging for this module
logger = logging.getLogger(__name__)

class HandRepository:
    def __init__(self, db_manager: DatabaseManager):
        self.db_manager = db_manager
        logger.debug("HandRepository initialized")
    
    def save(self, hand: PokerHand) -> PokerHand:
        """Save a poker hand to database"""
        logger.info(f"Saving poker hand with ID: {hand.id}")
        try:
            with self.db_manager.get_cursor() as cursor:
                logger.debug("Executing INSERT/UPDATE query for hand")
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
                if result:
                    hand.created_at = result['created_at']
                    logger.info(f"Hand saved successfully with created_at: {hand.created_at}")
                else:
                    logger.warning("No result returned from INSERT/UPDATE query")
                
                return hand
        except Exception as e:
            logger.error(f"Failed to save hand {hand.id}: {e}")
            logger.exception("Hand save error details:")
            raise e
    
    def get_all(self) -> List[PokerHand]:
        """Get all poker hands from database"""
        logger.info("Retrieving all poker hands from database")
        try:
            with self.db_manager.get_cursor() as cursor:
                logger.debug("Executing SELECT query for all hands")
                cursor.execute("""
                    SELECT id, stacks, dealer_index, small_blind_index, big_blind_index,
                           actions, hole_cards, board, winnings, created_at
                    FROM hands 
                    ORDER BY created_at DESC
                """)
                
                rows = cursor.fetchall()
                logger.info(f"Retrieved {len(rows)} rows from database")
                
                hands = []
                for i, row in enumerate(rows):
                    try:
                        hand = PokerHand(
                            id=row['id'],
                            stacks=list(row['stacks']) if row['stacks'] else [],
                            dealer_index=row['dealer_index'],
                            small_blind_index=row['small_blind_index'],
                            big_blind_index=row['big_blind_index'],
                            actions=list(row['actions']) if row['actions'] else [],
                            hole_cards=list(row['hole_cards']) if row['hole_cards'] else [],
                            board=row['board'] or "",
                            winnings=list(row['winnings']) if row['winnings'] else [],
                            created_at=row['created_at']
                        )
                        hands.append(hand)
                    except Exception as row_error:
                        logger.error(f"Error processing row {i}: {row_error}")
                        logger.exception(f"Row processing error details for row {i}:")
                        logger.error(f"Problematic row data: {row}")
                        # Continue with other rows instead of failing completely
                
                logger.info(f"Successfully processed {len(hands)} hands from {len(rows)} rows")
                return hands
                
        except Exception as e:
            logger.error(f"Failed to get all hands: {e}")
            logger.exception("Get all hands error details:")
            raise e
    
    def get_by_id(self, hand_id: str) -> Optional[PokerHand]:
        """Get a specific poker hand by ID"""
        logger.info(f"Retrieving poker hand with ID: {hand_id}")
        try:
            with self.db_manager.get_cursor() as cursor:
                logger.debug(f"Executing SELECT query for hand ID: {hand_id}")
                cursor.execute("""
                    SELECT id, stacks, dealer_index, small_blind_index, big_blind_index,
                           actions, hole_cards, board, winnings, created_at
                    FROM hands 
                    WHERE id = %s
                """, (hand_id,))
                
                row = cursor.fetchone()
                if not row:
                    logger.warning(f"No hand found with ID: {hand_id}")
                    return None
                
                logger.info(f"Successfully retrieved hand with ID: {hand_id}")
                return PokerHand(
                    id=row['id'],
                    stacks=list(row['stacks']) if row['stacks'] else [],
                    dealer_index=row['dealer_index'],
                    small_blind_index=row['small_blind_index'],
                    big_blind_index=row['big_blind_index'],
                    actions=list(row['actions']) if row['actions'] else [],
                    hole_cards=list(row['hole_cards']) if row['hole_cards'] else [],
                    board=row['board'] or "",
                    winnings=list(row['winnings']) if row['winnings'] else [],
                    created_at=row['created_at']
                )
                
        except Exception as e:
            logger.error(f"Failed to get hand {hand_id}: {e}")
            logger.exception("Get hand by ID error details:")
            raise e