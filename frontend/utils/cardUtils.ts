// frontend/utils/cardUtils.ts
export const SUITS = ['c', 'd', 'h', 's'] as const;
export const RANKS = ['2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K', 'A'] as const;

export type Suit = typeof SUITS[number];
export type Rank = typeof RANKS[number];
export type Card = `${Rank}${Suit}`;

export function generateDeck(): Card[] {
  const deck: Card[] = [];
  for (const rank of RANKS) {
    for (const suit of SUITS) {
      deck.push(`${rank}${suit}` as Card);
    }
  }
  return shuffleDeck(deck);
}

export function shuffleDeck(deck: Card[]): Card[] {
  const newDeck = [...deck];
  for (let i = newDeck.length - 1; i > 0; i--) {
    const j = Math.floor(Math.random() * (i + 1));
    [newDeck[i], newDeck[j]] = [newDeck[j], newDeck[i]];
  }
  return newDeck;
}

export function dealCards(deck: Card[], numPlayers: number): string[][] {
  const hands: string[][] = Array(numPlayers).fill(null).map(() => []);
  let deckIndex = 0;

  // Deal 2 cards to each player
  for (let round = 0; round < 2; round++) {
    for (let player = 0; player < numPlayers; player++) {
      if (deckIndex < deck.length) {
        hands[player].push(deck[deckIndex]);
        deckIndex++;
      }
    }
  }

  return hands;
}

export function formatCard(card: string): string {
  if (card.length !== 2) return card;
  
  const rank = card[0];
  const suit = card[1];
  
  const suitSymbol = {
    'c': '♣',
    'd': '♦',
    'h': '♥',
    's': '♠'
  }[suit] || suit;

  return `${rank}${suitSymbol}`;
}

export function formatCards(cards: string[]): string {
  return cards.map(formatCard).join(' ');
}