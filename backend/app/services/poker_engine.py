from typing import List, Dict, Tuple
from pokerkit import Automation, NoLimitTexasHoldem
import re


class PokerEngine:
    @staticmethod
    def calculate_winnings(
        hole_cards: List[str],  # List of hole cards for each player (empty string if folded)
        board_cards: str,  # Board cards as string "AsKdQc2h5s"
        actions: List[str],  # Action sequence
        starting_stacks: List[int]  # Starting stacks for each player
    ) -> Tuple[List[int], List[int]]:  # Returns (final_stacks, winnings)
        """
        Calculate final stacks and winnings using pokerkit
        """
        try:
            # Convert our format to pokerkit format
            num_players = len(starting_stacks)
            
            # Create the game state
            state = NoLimitTexasHoldem.create_state(
                # Automations
                (
                    Automation.ANTE_POSTING,
                    Automation.BET_COLLECTION,
                    Automation.BLIND_OR_STRADDLE_POSTING,
                    Automation.HOLE_CARDS_SHOWING_OR_MUCKING,
                    Automation.HAND_KILLING,
                    Automation.CHIPS_PUSHING,
                    Automation.CHIPS_PULLING,
                ),
                True,  # Uniform antes?
                0,  # Antes (we don't use antes)
                (20, 40),  # Blinds (small blind, big blind)
                40,  # Min-bet (big blind size)
                tuple(starting_stacks),  # Starting stacks
                num_players,  # Number of players
            )
            
            # Deal hole cards
            for i, cards in enumerate(hole_cards):
                if cards and len(cards) >= 4:  # If player has cards (didn't fold pre)
                    state.deal_hole(cards)
                else:
                    state.deal_hole('')  # Empty for folded players
            
            # Process actions
            for action in actions:
                if not action:
                    continue
                    
                action = action.strip()
                if action.startswith('f'):  # fold
                    state.fold()
                elif action.startswith('x'):  # check
                    state.check_or_call()
                elif action.startswith('c'):  # call
                    state.check_or_call()
                elif action.startswith('b'):  # bet
                    amount = int(re.findall(r'\d+', action)[0])
                    state.complete_bet_or_raise_to(amount)
                elif action.startswith('r'):  # raise
                    amount = int(re.findall(r'\d+', action)[0])
                    state.complete_bet_or_raise_to(amount)
                elif action == 'allin':
                    # Get current stack and go all-in
                    current_stack = state.stacks[state.actor_index]
                    state.complete_bet_or_raise_to(current_stack)
                elif len(action) >= 6 and PokerEngine._is_board_cards(action):
                    # Board cards (flop/turn/river)
                    if len(action) == 6:  # Flop (3 cards)
                        state.burn_card()
                        state.deal_board(action)
                    elif len(action) == 8:  # Turn (1 card)
                        state.burn_card()
                        state.deal_board(action[-2:])
                    elif len(action) == 10:  # River (1 card)
                        state.burn_card()
                        state.deal_board(action[-2:])
            
            # If we have board cards left, deal them
            if board_cards and len(board_cards) > len(''.join(re.findall(r'[A-Z][a-z]', ''.join(actions)))):
                remaining_board = board_cards
                for action in actions:
                    if PokerEngine._is_board_cards(action):
                        remaining_board = remaining_board[len(action):]
                
                while remaining_board and len(remaining_board) >= 2:
                    state.burn_card()
                    state.deal_board(remaining_board[:2])
                    remaining_board = remaining_board[2:]
            
            final_stacks = list(state.stacks)
            winnings = [final - start for final, start in zip(final_stacks, starting_stacks)]
            
            return final_stacks, winnings
            
        except Exception as e:
            # If pokerkit fails, return original stacks
            print(f"Poker engine error: {e}")
            winnings = [0] * len(starting_stacks)
            return starting_stacks, winnings
    
    @staticmethod
    def _is_board_cards(action: str) -> bool:
        """Check if action represents board cards"""
        # Board cards should be even length and contain valid card representations
        if len(action) % 2 != 0:
            return False
        
        # Check if it looks like cards (alternating ranks and suits)
        for i in range(0, len(action), 2):
            if i + 1 >= len(action):
                return False
            rank = action[i]
            suit = action[i + 1]
            if rank not in '23456789TJQKA' or suit not in 'cdhs':
                return False
        
        return True
    
    @staticmethod
    def format_action_sequence(actions: List[str]) -> str:
        """Format actions into short format for display"""
        formatted = []
        for action in actions:
            if action.startswith('f'):
                formatted.append('f')
            elif action.startswith('x'):
                formatted.append('x')
            elif action.startswith('c'):
                formatted.append('c')
            elif action.startswith('b'):
                amount = re.findall(r'\d+', action)
                formatted.append(f"b{amount[0]}" if amount else 'b')
            elif action.startswith('r'):
                amount = re.findall(r'\d+', action)
                formatted.append(f"r{amount[0]}" if amount else 'r')
            elif action == 'allin':
                formatted.append('allin')
            elif PokerEngine._is_board_cards(action):
                formatted.append(action)
            else:
                formatted.append(action)
        
        return ' '.join(formatted)