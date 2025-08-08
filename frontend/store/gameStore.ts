// frontend/store/gameStore.ts
'use client';

import { create } from 'zustand';
import { GameState, Player, PokerAction, SMALL_BLIND, BIG_BLIND, DEFAULT_STACK } from '../types/game';
import { dealCards, generateDeck } from '../utils/cardUtils';
import { saveHand } from '../utils/api';

interface GameStore extends GameState {
  // Actions
  resetGame: () => void;
  setPlayerStacks: (stacks: number[]) => void;
  startHand: () => void;
  performAction: (action: PokerAction) => Promise<void>;
  nextPhase: () => void;
  finishHand: () => Promise<void>;
  setBetAmount: (amount: number) => void;
  canPerformAction: (actionType: string) => boolean;
  getCurrentPlayer: () => Player;
  getNextActivePlayer: (startIndex: number) => number;
  isBettingRoundComplete: () => boolean;
}

const createInitialPlayers = (): Player[] => {
  return Array.from({ length: 6 }, (_, i) => ({
    id: i,
    name: `Player ${i + 1}`,
    stack: DEFAULT_STACK,
    holeCards: [],
    position: getPositionName(i, 0),
    isActive: true,
    isFolded: false,
    currentBet: 0,
    isAllIn: false,
  }));
};

const getPositionName = (playerIndex: number, dealerIndex: number): string => {
  const positions = ['Dealer', 'Small Blind', 'Big Blind', 'UTG', 'MP', 'CO'];
  const relativePosition = (playerIndex - dealerIndex + 6) % 6;
  return positions[relativePosition];
};

export const useGameStore = create<GameStore>((set, get) => ({
  // Initial state
  players: createInitialPlayers(),
  board: [],
  pot: 0,
  currentBet: 0,
  dealerIndex: 0,
  smallBlindIndex: 1,
  bigBlindIndex: 2,
  activePlayerIndex: 3, // UTG starts action preflop
  phase: 'setup',
  actions: [],
  handId: undefined,
  isHandStarted: false,
  betAmount: BIG_BLIND,

  resetGame: () => {
    set({
      players: createInitialPlayers(),
      board: [],
      pot: 0,
      currentBet: 0,
      dealerIndex: 0,
      smallBlindIndex: 1,
      bigBlindIndex: 2,
      activePlayerIndex: 3,
      phase: 'setup',
      actions: [],
      handId: undefined,
      isHandStarted: false,
      betAmount: BIG_BLIND,
    });
  },

  setPlayerStacks: (stacks: number[]) => {
    set((state) => ({
      players: state.players.map((player, i) => ({
        ...player,
        stack: stacks[i] || DEFAULT_STACK,
      })),
    }));
  },

  startHand: () => {
    const state = get();
    const deck = generateDeck();
    const dealtCards = dealCards(deck, 6);
    
    set({
      players: state.players.map((player, i) => ({
        ...player,
        holeCards: dealtCards[i] || [],
        position: getPositionName(i, state.dealerIndex),
        isActive: true,
        isFolded: false,
        currentBet: i === state.smallBlindIndex ? SMALL_BLIND : i === state.bigBlindIndex ? BIG_BLIND : 0,
        isAllIn: false,
      })),
      board: [],
      pot: SMALL_BLIND + BIG_BLIND,
      currentBet: BIG_BLIND,
      phase: 'preflop',
      actions: [`Player ${state.smallBlindIndex + 1} posts small blind ${SMALL_BLIND}`, `Player ${state.bigBlindIndex + 1} posts big blind ${BIG_BLIND}`],
      isHandStarted: true,
    });

    // Adjust stacks for blinds
    set((state) => ({
      players: state.players.map((player, i) => ({
        ...player,
        stack: i === state.smallBlindIndex ? player.stack - SMALL_BLIND : 
               i === state.bigBlindIndex ? player.stack - BIG_BLIND : 
               player.stack,
      })),
    }));
  },

  performAction: async (action: PokerAction) => {
    const state = get();
    const currentPlayer = state.players[state.activePlayerIndex];
    
    if (!currentPlayer || currentPlayer.isFolded || !currentPlayer.isActive) {
      return;
    }

    let actionString = '';
    let newStack = currentPlayer.stack;
    let newBet = currentPlayer.currentBet;
    let potIncrease = 0;
    let newCurrentBet = state.currentBet;
    let playerFolded = false;

    switch (action.type) {
      case 'fold':
        playerFolded = true;
        actionString = `Player ${currentPlayer.id + 1} folds`;
        break;
        
      case 'check':
        if (state.currentBet === currentPlayer.currentBet) {
          actionString = `Player ${currentPlayer.id + 1} checks`;
        } else {
          return; // Can't check if there's a bet to call
        }
        break;
        
      case 'call':
        const callAmount = state.currentBet - currentPlayer.currentBet;
        const actualCall = Math.min(callAmount, currentPlayer.stack);
        newStack -= actualCall;
        newBet = currentPlayer.currentBet + actualCall;
        potIncrease = actualCall;
        actionString = `Player ${currentPlayer.id + 1} calls ${actualCall}`;
        break;
        
      case 'bet':
        if (state.currentBet > 0) return; // Can't bet if there's already a bet
        const betAmount = action.amount || state.betAmount;
        const actualBet = Math.min(betAmount, currentPlayer.stack);
        newStack -= actualBet;
        newBet = actualBet;
        newCurrentBet = actualBet;
        potIncrease = actualBet;
        actionString = `Player ${currentPlayer.id + 1} bets ${actualBet}`;
        break;
        
      case 'raise':
        const raiseAmount = action.amount || state.betAmount;
        const totalRaise = Math.min(raiseAmount, currentPlayer.stack + currentPlayer.currentBet);
        const raiseIncrease = totalRaise - currentPlayer.currentBet;
        newStack -= raiseIncrease;
        newBet = totalRaise;
        newCurrentBet = totalRaise;
        potIncrease = raiseIncrease;
        actionString = `Player ${currentPlayer.id + 1} raises to ${totalRaise}`;
        break;
        
      case 'allin':
        const allInAmount = currentPlayer.stack + currentPlayer.currentBet;
        potIncrease = currentPlayer.stack;
        newStack = 0;
        newBet = allInAmount;
        if (allInAmount > state.currentBet) {
          newCurrentBet = allInAmount;
        }
        actionString = `Player ${currentPlayer.id + 1} goes all-in ${allInAmount}`;
        break;
    }

    // Update game state
    set((state) => ({
      players: state.players.map((player, i) => 
        i === state.activePlayerIndex ? {
          ...player,
          stack: newStack,
          currentBet: newBet,
          isFolded: playerFolded,
          isAllIn: newStack === 0 && !playerFolded,
        } : player
      ),
      pot: state.pot + potIncrease,
      currentBet: newCurrentBet,
      actions: [...state.actions, actionString],
      activePlayerIndex: get().getNextActivePlayer(state.activePlayerIndex),
    }));

    // Check if betting round is complete
    const updatedState = get();
    if (get().isBettingRoundComplete()) {
      setTimeout(() => {
        get().nextPhase();
      }, 500);
    }
  },

  nextPhase: () => {
    const state = get();
    let newPhase = state.phase;
    let newBoard = [...state.board];
    let newActivePlayerIndex = state.smallBlindIndex;
    let actionLog = '';

    // Reset bets for new round
    const resetPlayers = state.players.map(player => ({
      ...player,
      currentBet: 0,
    }));

    switch (state.phase) {
      case 'preflop':
        newPhase = 'flop';
        const flopCards = ['As', 'Kd', 'Qh']; // In real implementation, deal from deck
        newBoard = flopCards;
        actionLog = `Flop: ${flopCards.join(' ')}`;
        break;
        
      case 'flop':
        newPhase = 'turn';
        const turnCard = 'Jc'; // In real implementation, deal from deck
        newBoard = [...state.board, turnCard];
        actionLog = `Turn: ${turnCard}`;
        break;
        
      case 'turn':
        newPhase = 'river';
        const riverCard = 'Ts'; // In real implementation, deal from deck
        newBoard = [...state.board, riverCard];
        actionLog = `River: ${riverCard}`;
        break;
        
      case 'river':
        newPhase = 'showdown';
        actionLog = 'Showdown';
        setTimeout(() => {
          get().finishHand();
        }, 1000);
        break;
    }

    set({
      phase: newPhase,
      board: newBoard,
      currentBet: 0,
      players: resetPlayers,
      activePlayerIndex: newActivePlayerIndex,
      actions: actionLog ? [...state.actions, actionLog] : state.actions,
    });
  },

  finishHand: async () => {
    const state = get();
    
    try {
      // Save hand to backend
      await saveHand({
        stacks: state.players.map(p => p.stack + (p.stack === 0 && p.isAllIn ? p.currentBet : 0)),
        dealer_index: state.dealerIndex,
        small_blind_index: state.smallBlindIndex,
        big_blind_index: state.bigBlindIndex,
        actions: state.actions,
        hole_cards: state.players.map(p => p.holeCards.join('')),
        board: state.board.join(''),
      });
    } catch (error) {
      console.error('Failed to save hand:', error);
    }

    set({ phase: 'finished' });
  },

  setBetAmount: (amount: number) => {
    set({ betAmount: amount });
  },

  canPerformAction: (actionType: string): boolean => {
    const state = get();
    const currentPlayer = state.players[state.activePlayerIndex];
    
    if (!currentPlayer || currentPlayer.isFolded || !currentPlayer.isActive || state.phase === 'finished') {
      return false;
    }

    switch (actionType) {
      case 'fold':
        return true;
      case 'check':
        return state.currentBet === currentPlayer.currentBet;
      case 'call':
        return state.currentBet > currentPlayer.currentBet && currentPlayer.stack > 0;
      case 'bet':
        return state.currentBet === 0 && currentPlayer.stack > 0;
      case 'raise':
        return state.currentBet > 0 && currentPlayer.stack > 0;
      case 'allin':
        return currentPlayer.stack > 0;
      default:
        return false;
    }
  },

  getCurrentPlayer: (): Player => {
    const state = get();
    return state.players[state.activePlayerIndex];
  },

  getNextActivePlayer: (startIndex: number): number => {
    const state = get();
    let nextIndex = (startIndex + 1) % 6;
    let attempts = 0;
    
    while (attempts < 6) {
      const player = state.players[nextIndex];
      if (!player.isFolded && player.isActive && !player.isAllIn) {
        return nextIndex;
      }
      nextIndex = (nextIndex + 1) % 6;
      attempts++;
    }
    
    return startIndex; // Fallback
  },

  // Helper method to check if betting round is complete
  isBettingRoundComplete: (): boolean => {
    const state = get();
    const activePlayers = state.players.filter(p => !p.isFolded && p.isActive);
    
    if (activePlayers.length <= 1) return true;
    
    const playersStillToAct = activePlayers.filter(p => 
      !p.isAllIn && p.currentBet < state.currentBet
    );
    
    // All active players have either folded, gone all-in, or matched the current bet
    return playersStillToAct.length === 0;
  },
}));