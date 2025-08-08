from fastapi import APIRouter, HTTPException, Depends
from typing import List
from app.schemas.hand import PokerHandCreate, PokerHandResponse, PokerHandUpdate
from app.models.hand import PokerHand
from app.repositories.hand_repository import HandRepository
from app.services.poker_engine import PokerEngine
from app.core.db import db_manager


router = APIRouter()


def get_hand_repository() -> HandRepository:
    return HandRepository(db_manager)


@router.post("/", response_model=PokerHandResponse)
def create_hand(
    hand_data: PokerHandCreate,
    repository: HandRepository = Depends(get_hand_repository)
):
    """Create a new poker hand and calculate winnings"""
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
        
        # Calculate winnings using poker engine
        try:
            final_stacks, winnings = PokerEngine.calculate_winnings(
                hole_cards=hand.hole_cards,
                board_cards=hand.board,
                actions=hand.actions,
                starting_stacks=hand.stacks
            )
            hand.winnings = winnings
        except Exception as e:
            # If poker calculation fails, set winnings to zero
            print(f"Poker calculation failed: {e}")
            hand.winnings = [0] * len(hand.stacks)
        
        # Save to database
        saved_hand = repository.save(hand)
        
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
        raise HTTPException(status_code=400, detail=f"Failed to create hand: {str(e)}")


@router.get("/", response_model=List[PokerHandResponse])
def get_hands(
    repository: HandRepository = Depends(get_hand_repository)
):
    """Get all poker hands"""
    try:
        hands = repository.get_all()
        return [
            PokerHandResponse(
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
            for hand in hands
        ]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get hands: {str(e)}")


@router.get("/{hand_id}", response_model=PokerHandResponse)
def get_hand(
    hand_id: str,
    repository: HandRepository = Depends(get_hand_repository)
):
    """Get a specific poker hand"""
    try:
        hand = repository.get_by_id(hand_id)
        if not hand:
            raise HTTPException(status_code=404, detail="Hand not found")
            
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
        raise HTTPException(status_code=500, detail=f"Failed to get hand: {str(e)}")