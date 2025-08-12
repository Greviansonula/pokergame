// frontend/utils/api.ts
import { HandHistory } from '../types/game';

const API_BASE = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

export interface CreateHandRequest {
  stacks: number[];
  dealer_index: number;
  small_blind_index: number;
  big_blind_index: number;
  actions: string[];
  hole_cards: string[];
  board: string;
}

export async function saveHand(handData: CreateHandRequest): Promise<HandHistory> {
  const response = await fetch(`${API_BASE}/api/v1/hands/`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(handData),
  });

  if (!response.ok) {
    throw new Error(`Failed to save hand: ${response.statusText}`);
  }

  return response.json();
}

export async function getHands(): Promise<HandHistory[]> {
  const response = await fetch(`${API_BASE}/api/v1/hands/`);
  
  if (!response.ok) {
    throw new Error(`Failed to get hands: ${response.statusText}`);
  }

  return response.json();
}

export async function getHand(handId: string): Promise<HandHistory> {
  const response = await fetch(`${API_BASE}/api/v1/hands/${handId}`);
  
  if (!response.ok) {
    throw new Error(`Failed to get hand: ${response.statusText}`);
  }

  return response.json();
}