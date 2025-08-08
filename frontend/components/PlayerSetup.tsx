// frontend/components/PlayerSetup.tsx
'use client';

import { useState } from 'react';
import { Button } from './ui/button';
import { Input } from './ui/input';
import { Label } from './ui/label';
import { Card, CardContent, CardHeader, CardTitle } from './ui/card';
import { useGameStore } from '../store/gameStore';
import { DEFAULT_STACK } from '../types/game';

export function PlayerSetup() {
  const { players, setPlayerStacks, startHand, resetGame, isHandStarted } = useGameStore();
  const [stacks, setStacks] = useState<number[]>(players.map(p => p.stack));

  const handleStackChange = (index: number, value: string) => {
    const newStacks = [...stacks];
    newStacks[index] = parseInt(value) || 0;
    setStacks(newStacks);
    setPlayerStacks(newStacks);
  };

  const handleReset = () => {
    resetGame();
    setStacks(Array(6).fill(DEFAULT_STACK));
  };

  const handleStart = () => {
    setPlayerStacks(stacks);
    startHand();
  };

  return (
    <Card className="w-full">
      <CardHeader>
        <CardTitle>Player Setup</CardTitle>
      </CardHeader>
      <CardContent>
        <div className="grid grid-cols-2 gap-4 mb-4">
          {players.map((player, index) => (
            <div key={player.id} className="flex items-center space-x-2">
              <Label htmlFor={`stack-${index}`} className="w-20 text-sm">
                {player.name}:
              </Label>
              <Input
                id={`stack-${index}`}
                type="number"
                value={stacks[index]}
                onChange={(e) => handleStackChange(index, e.target.value)}
                className="w-24"
                min="0"
                step="1"
              />
              <span className="text-sm text-muted-foreground">chips</span>
            </div>
          ))}
        </div>
        
        <div className="flex space-x-2">
          <Button 
            onClick={handleStart} 
            disabled={isHandStarted}
            className="flex-1"
          >
            {isHandStarted ? 'Hand In Progress' : 'Start'}
          </Button>
          <Button 
            onClick={handleReset} 
            variant="outline"
            className="flex-1"
          >
            {isHandStarted ? 'Reset' : 'Reset'}
          </Button>
        </div>
        
        {isHandStarted && (
          <div className="mt-4 p-3 bg-muted rounded-md">
            <h4 className="font-semibold text-sm mb-2">Current Positions:</h4>
            <div className="grid grid-cols-2 gap-1 text-xs">
              {players.map((player, index) => (
                <div key={player.id} className="flex justify-between">
                  <span>{player.name}:</span>
                  <span className="font-mono">{player.position}</span>
                </div>
              ))}
            </div>
          </div>
        )}
      </CardContent>
    </Card>
  );
}