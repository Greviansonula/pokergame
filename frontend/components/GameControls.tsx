// frontend/components/GameControls.tsx
'use client';

import { Button } from './ui/button';
import { Input } from './ui/input';
import { Label } from './ui/label';
import { Card, CardContent, CardHeader, CardTitle } from './ui/card';
import { useGameStore } from '../store/gameStore';
import { Minus, Plus } from 'lucide-react';
import { BIG_BLIND } from '../types/game';

export function GameControls() {
  const {
    performAction,
    canPerformAction,
    getCurrentPlayer,
    betAmount,
    setBetAmount,
    phase,
    currentBet,
    isHandStarted
  } = useGameStore();

  const currentPlayer = getCurrentPlayer();

  const handleAction = async (type: string, amount?: number) => {
    await performAction({
      type: type as any,
      amount,
      playerId: currentPlayer?.id || 0,
    });
  };

  const adjustBetAmount = (increment: boolean) => {
    const newAmount = increment ? betAmount + BIG_BLIND : Math.max(BIG_BLIND, betAmount - BIG_BLIND);
    setBetAmount(newAmount);
  };

  if (!isHandStarted || phase === 'finished') {
    return (
      <Card className="w-full">
        <CardHeader>
          <CardTitle>Game Controls</CardTitle>
        </CardHeader>
        <CardContent>
          <div className="text-center text-muted-foreground">
            {phase === 'finished' ? 'Hand finished' : 'Start a hand to begin playing'}
          </div>
        </CardContent>
      </Card>
    );
  }

  return (
    <Card className="w-full">
      <CardHeader>
        <CardTitle>Game Controls</CardTitle>
        {currentPlayer && (
          <div className="text-sm text-muted-foreground">
            Current Player: {currentPlayer.name} (Stack: {currentPlayer.stack})
            <br />
            Phase: {phase.charAt(0).toUpperCase() + phase.slice(1)}
            <br />
            Current Bet: {currentBet}
          </div>
        )}
      </CardHeader>
      <CardContent>
        <div className="grid grid-cols-2 gap-2 mb-4">
          <Button
            onClick={() => handleAction('fold')}
            disabled={!canPerformAction('fold')}
            variant="destructive"
            size="sm"
          >
            Fold
          </Button>
          
          <Button
            onClick={() => handleAction('check')}
            disabled={!canPerformAction('check')}
            variant="outline"
            size="sm"
          >
            Check
          </Button>
          
          <Button
            onClick={() => handleAction('call')}
            disabled={!canPerformAction('call')}
            variant="secondary"
            size="sm"
          >
            Call {currentPlayer ? Math.min(currentBet - currentPlayer.currentBet, currentPlayer.stack) : 0}
          </Button>
          
          <Button
            onClick={() => handleAction('allin')}
            disabled={!canPerformAction('allin')}
            variant="outline"
            size="sm"
          >
            All-in
          </Button>
        </div>

        <div className="space-y-3">
          {/* Bet Amount Controls */}
          <div className="flex items-center space-x-2">
            <Label htmlFor="bet-amount" className="text-sm">Amount:</Label>
            <Button
              size="icon"
              variant="outline"
              className="h-8 w-8"
              onClick={() => adjustBetAmount(false)}
            >
              <Minus className="h-4 w-4" />
            </Button>
            <Input
              id="bet-amount"
              type="number"
              value={betAmount}
              onChange={(e) => setBetAmount(parseInt(e.target.value) || BIG_BLIND)}
              className="w-20 h-8 text-center"
              min={BIG_BLIND}
              step={BIG_BLIND}
            />
            <Button
              size="icon"
              variant="outline"
              className="h-8 w-8"
              onClick={() => adjustBetAmount(true)}
            >
              <Plus className="h-4 w-4" />
            </Button>
          </div>

          {/* Bet and Raise buttons */}
          <div className="grid grid-cols-2 gap-2">
            <Button
              onClick={() => handleAction('bet', betAmount)}
              disabled={!canPerformAction('bet')}
              size="sm"
            >
              Bet {betAmount}
            </Button>
            
            <Button
              onClick={() => handleAction('raise', betAmount)}
              disabled={!canPerformAction('raise')}
              size="sm"
            >
              Raise to {betAmount}
            </Button>
          </div>
        </div>

        {/* Game State Info */}
        {currentPlayer && (
          <div className="mt-4 p-3 bg-muted rounded-md text-xs">
            <div className="flex justify-between mb-1">
              <span>Player Bet:</span>
              <span>{currentPlayer.currentBet}</span>
            </div>
            <div className="flex justify-between mb-1">
              <span>To Call:</span>
              <span>{Math.max(0, currentBet - currentPlayer.currentBet)}</span>
            </div>
            <div className="flex justify-between">
              <span>Can Call:</span>
              <span>{canPerformAction('call') ? 'Yes' : 'No'}</span>
            </div>
          </div>
        )}
      </CardContent>
    </Card>
  );
}