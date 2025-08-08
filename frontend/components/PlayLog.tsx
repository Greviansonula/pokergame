// frontend/components/PlayLog.tsx
'use client';

import { useEffect, useRef } from 'react';
import { Card, CardContent, CardHeader, CardTitle } from './ui/card';
import { useGameStore } from '../store/gameStore';
import { formatCards } from '../utils/cardUtils';

export function PlayLog() {
  const { actions, board, players, phase, pot } = useGameStore();
  const scrollRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    if (scrollRef.current) {
      scrollRef.current.scrollTop = scrollRef.current.scrollHeight;
    }
  }, [actions]);

  const getCurrentHandInfo = () => {
    const info = [];
    
    if (phase !== 'setup') {
      info.push(`Phase: ${phase.charAt(0).toUpperCase() + phase.slice(1)}`);
      info.push(`Pot: ${pot} chips`);
      
      if (board.length > 0) {
        info.push(`Board: ${formatCards(board)}`);
      }
      
      // Show player hole cards (in real game, this would be hidden)
      const playersWithCards = players.filter(p => p.holeCards.length > 0);
      if (playersWithCards.length > 0) {
        info.push('---');
        playersWithCards.forEach(player => {
          if (!player.isFolded) {
            info.push(`${player.name}: ${formatCards(player.holeCards)} (${player.stack} chips)`);
          }
        });
      }
    }
    
    return info;
  };

  const currentInfo = getCurrentHandInfo();

  return (
    <Card className="w-full h-96">
      <CardHeader>
        <CardTitle>Play Log</CardTitle>
      </CardHeader>
      <CardContent>
        <div
          ref={scrollRef}
          className="h-full overflow-y-auto space-y-1 text-sm font-mono bg-muted p-3 rounded"
        >
          {actions.length === 0 && phase === 'setup' && (
            <div className="text-muted-foreground">
              Start a hand to see the action log...
            </div>
          )}
          
          {currentInfo.map((info, index) => (
            <div
              key={`info-${index}`}
              className={info === '---' ? 'border-t border-border my-2' : 'text-primary'}
            >
              {info !== '---' && info}
            </div>
          ))}
          
          {currentInfo.length > 0 && actions.length > 0 && (
            <div className="border-t border-border my-2"></div>
          )}
          
          {actions.map((action, index) => (
            <div
              key={index}
              className={`${
                action.includes('Flop') || action.includes('Turn') || action.includes('River') || action.includes('Showdown')
                  ? 'text-blue-600 font-semibold'
                  : action.includes('folds')
                  ? 'text-red-600'
                  : action.includes('bets') || action.includes('raises')
                  ? 'text-green-600'
                  : action.includes('posts')
                  ? 'text-orange-600'
                  : ''
              }`}
            >
              {action}
            </div>
          ))}
          
          {phase === 'finished' && (
            <div className="mt-4 p-2 bg-green-100 text-green-800 rounded">
              Hand completed! Check the hand history for final results.
            </div>
          )}
        </div>
      </CardContent>
    </Card>
  );
}