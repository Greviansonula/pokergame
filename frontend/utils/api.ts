// frontend/utils/api.ts
import { HandHistory } from '../types/game';

// Use local Next.js API routes that will proxy to the backend
const API_BASE = '/api';

console.log('API_BASE configured as:', API_BASE);
console.log('Using local Next.js API routes for proxying to backend');

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
  const url = `${API_BASE}/hands/`;
  console.log('Making API call to local route:', url);
  console.log('Request data:', handData);
  
  try {
    const response = await fetch(url, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(handData),
    });

    console.log('Response status:', response.status);
    console.log('Response headers:', Object.fromEntries(response.headers.entries()));

    if (!response.ok) {
      const errorText = await response.text();
      console.error('API Error Response:', errorText);
      throw new Error(`Failed to save hand: ${response.statusText}`);
    }

    const result = await response.json();
    console.log('API call successful:', result);
    return result;
  } catch (error) {
    console.error('Fetch error details:', error);
    console.error('Error type:', typeof error);
    console.error('Error constructor:', error?.constructor?.name);
    if (error instanceof TypeError) {
      console.error('This is a network/fetch error');
    }
    throw error;
  }
}

export async function getHands(): Promise<HandHistory[]> {
  const url = `${API_BASE}/hands/`;
  console.log('Making API call to local route:', url);
  console.log('Current API_BASE:', API_BASE);
  
  try {
    console.log('Starting fetch request...');
    const response = await fetch(url);
    
    console.log('Response received:', response);
    console.log('Response status:', response.status);
    console.log('Response ok:', response.ok);
    console.log('Response headers:', Object.fromEntries(response.headers.entries()));
    
    if (!response.ok) {
      const errorText = await response.text();
      console.error('API Error Response:', errorText);
      throw new Error(`Failed to get hands: ${response.statusText}`);
    }

    const result = await response.json();
    console.log('API call successful, hands count:', result.length);
    return result;
  } catch (error) {
    console.error('Fetch error in getHands:', error);
    console.error('Error type:', typeof error);
    console.error('Error constructor:', error?.constructor?.name);
    console.error('Error message:', (error as Error)?.message);
    console.error('Error stack:', (error as Error)?.stack);
    
    if (error instanceof TypeError) {
      console.error('This is a network/fetch error - likely CORS or connection issue');
    }
    
    throw error;
  }
}

export async function getHand(handId: string): Promise<HandHistory> {
  const url = `${API_BASE}/hands/${handId}`;
  console.log('Making API call to local route:', url);
  
  try {
    const response = await fetch(url);
    
    if (!response.ok) {
      const errorText = await response.text();
      console.error('API Error Response:', errorText);
      throw new Error(`Failed to get hand: ${response.statusText}`);
    }

    const result = await response.json();
    console.log('API call successful:', result);
    return result;
  } catch (error) {
    console.error('Fetch error in getHand:', error);
    throw error;
  }
}