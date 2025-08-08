// frontend/components/HandHistory.tsx
'use client';

import { useState, useEffect } from 'react';
import { Card, CardContent, CardHeader, CardTitle } from './ui/card';
import { Button } from './ui/button';
import { HandHistory as HandHistoryType } from '../types/game';
import { getHands } from '../utils/api';
import { formatCards } from '../utils/cardUtils';
import { RefreshCw } from 'lucide-react';

export function HandHistory() {
  const [hands, setHands] = useState<HandHistoryType[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const loadHands = async () => {
    setLoading(true);
    setError(null);
    try {
      const fetchedHands = await getHands();
      setHands(fetchedHands);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to load hands');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadHands();
  }, []);

  const formatHandHistory = (hand: HandHistoryType) => {
    const lines = [];
    
    // Line 1: Hand UUID
    lines.push(`Hand: ${hand.id.substring(0, 8)}...`);
    
    // Line 2: Stack settings and positions
    const dealer = `Dealer: P${hand.dealer_index + 1}`;
    const sb = `SB: P${hand.small_blind_index + 1}`;
    const bb = `BB: P${hand.big_blind_index + 1}`;
    const stackInfo = `Stacks: ${hand.stacks.join('/')}`;
    lines.push(`${stackInfo} | ${dealer}, ${sb}, ${bb}`);
    
    // Line 3: Hole cards
    const holeCardsFormatted = hand.hole_cards.map((cards, i) => 
      cards ? `P${i + 1}:${formatCards([cards.slice(0, 2), cards.slice(2, 4)].filter(c => c))}` : `P${i + 1}:-`
    ).join(' ');
    lines.push(`Cards: ${holeCardsFormatted}`);
    
    // Line 4: Action sequence (short format)
    const shortActions = formatShortActions(hand.actions);
    lines.push(`Actions: ${shortActions}`);
    
    // Line 5: Winnings
    const winnings = hand.winnings.map((w, i) => 
      w !== 0 ? `P${i + 1}:${w > 0 ? '+' : ''}${w}` : ''
    ).filter(w => w).join(' ');
    lines.push(`Result: ${winnings || 'No winnings calculated'}`);
    
    return lines;
  };

  const formatShortActions = (actions: string[]): string => {
    return actions.map(action => {
      const actionLower = action.toLowerCase();
      if (actionLower.includes('fold')) return 'f';
      if (actionLower.includes('check')) return 'x';
      if (actionLower.includes('call')) return 'c';
      if (actionLower.includes('bet')) {
        const match = action.match(/bets? (\d+)/);
        return match ? `b${match[1]}` : 'b';
      }
      if (actionLower.includes('raise')) {
        const match = action.match(/raises? (?:to )?(\d+)/);
        return match ? `r${match[1]}` : 'r';
      }
      if (actionLower.includes('all-in') || actionLower.includes('allin')) return 'allin';
      if (actionLower.includes('flop:')) {
        const match = action.match(/flop: (.+)/i);
        return match ? match[1].replace(/\s/g, '') : 'flop';
      }
      if (actionLower.includes('turn:')) {
        const match = action.match(/turn: (.+)/i);
        return match ? match[1].replace(/\s/g, '') : 'turn';
      }
      if (actionLower.includes('river:')) {
        const match = action.match(/river: (.+)/i);
        return match ? match[1].replace(/\s/g, '') : 'river';
      }
      return '';
    }).filter(a => a).join(' ');
  };

  return (
    <Card className="w-full h-96">
      <CardHeader>
        <CardTitle className="flex items-center justify-between">
          Hand History
          <Button
            size="sm"
            variant="outline"
            onClick={loadHands}
            disabled={loading}
          >
            <RefreshCw className={`h-4 w-4 ${loading ? 'animate-spin' : ''}`} />
          </Button>
        </CardTitle>
      </CardHeader>
      <CardContent>
        <div className="h-full overflow-y-auto space-y-4">
          {loading && hands.length === 0 && (
            <div className="text-center text-muted-foreground">
              Loading hands...
            </div>
          )}
          
          {error && (
            <div className="text-center text-red-500 text-sm">
              Error: {error}
            </div>
          )}
          
          {!loading && hands.length === 0 && !error && (
            <div className="text-center text-muted-foreground">
              No hands played yet. Complete a hand to see history here.
            </div>
          )}
          
          {hands.map((hand) => {
            const handLines = formatHandHistory(hand);
            return (
              <div
                key={hand.id}
                className="border border-border rounded-md p-3 bg-muted/50 text-xs font-mono space-y-1"
              >
                {handLines.map((line, index) => (
                  <div
                    key={index}
                    className={`${
                      index === 0 ? 'font-semibold text-primary' :
                      index === 1 ? 'text-blue-600' :
                      index === 2 ? 'text-green-600' :
                      index === 3 ? 'text-purple-600' :
                      'text-orange-600'
                    }`}
                  >
                    {line}
                  </div>
                ))}
                <div className="text-xs text-muted-foreground mt-2">
                  {new Date(hand.created_at).toLocaleString()}
                </div>
              </div>
            );
          })}
        </div>
      </CardContent>
    </Card>
  );
}