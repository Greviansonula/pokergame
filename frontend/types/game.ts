// frontend/types/game.ts
export interface Player {
    id: number;
    name: string;
    stack: number;
    holeCards: string[];
    position: string;
    isActive: boolean;
    isFolded: boolean;
    currentBet: number;
    isAllIn: boolean;
  }
  
  export interface GameState {
    players: Player[];
    board: string[];
    pot: number;
    currentBet: number;
    dealerIndex: number;
    smallBlindIndex: number;
    bigBlindIndex: number;
    activePlayerIndex: number;
    phase: 'setup' | 'preflop' | 'flop' | 'turn' | 'river' | 'showdown' | 'finished';
    actions: string[];
    handId?: string;
    isHandStarted: boolean;
    betAmount: number;
  }
  
  export interface PokerAction {
    type: 'fold' | 'check' | 'call' | 'bet' | 'raise' | 'allin';
    amount?: number;
    playerId: number;
  }
  
  export interface HandHistory {
    id: string;
    stacks: number[];
    dealer_index: number;
    small_blind_index: number;
    big_blind_index: number;
    actions: string[];
    hole_cards: string[];
    board: string;
    winnings: number[];
    created_at: string;
  }
  
  export const SMALL_BLIND = 20;
  export const BIG_BLIND = 40;
  export const DEFAULT_STACK = 1000;