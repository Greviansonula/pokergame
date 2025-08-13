from fastapi import APIRouter, HTTPException, Depends
from typing import List
from app.schemas.hand import PokerHandCreate, PokerHandResponse, PokerHandUpdate
from app.models.hand import PokerHand
from app.repositories.hand_repository import HandRepository
from app.services.poker_engine import PokerEngine
from app.core.db import db_manager
import logging

# Configure logging for this module
logger = logging.getLogger(__name__)

router = APIRouter()


def get_hand_repository() -> HandRepository:
    return HandRepository(db_manager)


@router.post("/", response_model=PokerHandResponse)
def create_hand(
    hand_data: PokerHandCreate,
    repository: HandRepository = Depends(get_hand_repository)
):
    """Create a new poker hand and calculate winnings"""
    logger.info(f"Creating new poker hand with {len(hand_data.stacks)} players")
    try:
        # Create hand from input data
        hand = PokerHand(
            stacks=hand_data.stacks,
            dealer_index=hand_data.dealer_index,
            small_blind_index=hand_data.small_blind_index,
            big_blind_index=hand_data.big_blind_index,
            actions=hand_data.actions,
            hole_cards=hand_data.hole_cards,
            board=hand_data.board
        )
        logger.debug(f"PokerHand object created with ID: {hand.id}")
        
        # Calculate winnings using poker engine
        try:
            logger.debug("Calculating winnings using poker engine")
            final_stacks, winnings = PokerEngine.calculate_winnings(
                hole_cards=hand.hole_cards,
                board_cards=hand.board,
                actions=hand.actions,
                starting_stacks=hand.stacks
            )
            hand.winnings = winnings
            logger.info(f"Winnings calculated successfully: {winnings}")
        except Exception as e:
            # If poker calculation fails, set winnings to zero
            logger.warning(f"Poker calculation failed: {e}")
            logger.exception("Poker calculation error details:")
            hand.winnings = [0] * len(hand.stacks)
        
        # Save to database
        logger.debug("Saving hand to database")
        saved_hand = repository.save(hand)
        logger.info(f"Hand saved successfully with ID: {saved_hand.id}")
        
        return PokerHandResponse(
            id=saved_hand.id,
            stacks=saved_hand.stacks,
            dealer_index=saved_hand.dealer_index,
            small_blind_index=saved_hand.small_blind_index,
            big_blind_index=saved_hand.big_blind_index,
            actions=saved_hand.actions,
            hole_cards=saved_hand.hole_cards,
            board=saved_hand.board,
            winnings=saved_hand.winnings,
            created_at=saved_hand.created_at
        )
        
    except Exception as e:
        logger.error(f"Failed to create hand: {e}")
        logger.exception("Hand creation error details:")
        raise HTTPException(status_code=400, detail=f"Failed to create hand: {str(e)}")


@router.get("/", response_model=List[PokerHandResponse])
def get_hands(
    repository: HandRepository = Depends(get_hand_repository)
):
    """Get all poker hands"""
    logger.info("Retrieving all poker hands")
    try:
        logger.debug("Calling repository.get_all()")
        hands = repository.get_all()
        logger.info(f"Successfully retrieved {len(hands)} hands from database")
        
        # Convert to response models
        response_hands = []
        for hand in hands:
            try:
                response_hand = PokerHandResponse(
                    id=hand.id,
                    stacks=hand.stacks,
                    dealer_index=hand.dealer_index,
                    small_blind_index=hand.small_blind_index,
                    big_blind_index=hand.big_blind_index,
                    actions=hand.actions,
                    hole_cards=hand.hole_cards,
                    board=hand.board,
                    winnings=hand.winnings,
                    created_at=hand.created_at
                )
                response_hands.append(response_hand)
            except Exception as hand_error:
                logger.error(f"Error converting hand {hand.id} to response model: {hand_error}")
                logger.exception("Hand conversion error details:")
                # Continue with other hands instead of failing completely
        
        logger.info(f"Successfully converted {len(response_hands)} hands to response models")
        return response_hands
        
    except Exception as e:
        logger.error(f"Failed to get hands: {e}")
        logger.exception("Get hands error details:")
        raise HTTPException(status_code=500, detail=f"Failed to get hands: {str(e)}")


@router.get("/{hand_id}", response_model=PokerHandResponse)
def get_hand(
    hand_id: str,
    repository: HandRepository = Depends(get_hand_repository)
):
    """Get a specific poker hand"""
    logger.info(f"Retrieving poker hand with ID: {hand_id}")
    try:
        logger.debug(f"Calling repository.get_by_id({hand_id})")
        hand = repository.get_by_id(hand_id)
        if not hand:
            logger.warning(f"Hand not found with ID: {hand_id}")
            raise HTTPException(status_code=404, detail="Hand not found")
        
        logger.info(f"Successfully retrieved hand with ID: {hand_id}")
        return PokerHandResponse(
            id=hand.id,
            stacks=hand.stacks,
            dealer_index=hand.dealer_index,
            small_blind_index=hand.small_blind_index,
            big_blind_index=hand.big_blind_index,
            actions=hand.actions,
            hole_cards=hand.hole_cards,
            board=hand.board,
            winnings=hand.winnings,
            created_at=hand.created_at
        )
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to get hand {hand_id}: {e}")
        logger.exception("Get hand error details:")
        raise HTTPException(status_code=500, detail=f"Failed to get hand: {str(e)}")