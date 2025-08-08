// frontend/app/page.tsx
'use client';

import { PlayerSetup } from '../components/PlayerSetup';
import { GameControls } from '../components/GameControls';
import { PlayLog } from '../components/PlayLog';
import { HandHistory } from '../components/HandHistory';

export default function PokerGame() {
  return (
    <div className="min-h-screen bg-background p-4">
      <div className="max-w-7xl mx-auto">
        <header className="mb-6">
          <h1 className="text-3xl font-bold text-center">Texas Hold'em Poker</h1>
          <p className="text-center text-muted-foreground mt-2">
            6-Player Simplified Poker Game
          </p>
        </header>

        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          {/* Left Column - Setup and Controls */}
          <div className="space-y-6">
            <PlayerSetup />
            <GameControls />
          </div>

          {/* Middle Column - Play Log */}
          <div>
            <PlayLog />
          </div>

          {/* Right Column - Hand History */}
          <div>
            <HandHistory />
          </div>
        </div>

        <footer className="mt-8 text-center text-sm text-muted-foreground">
          <p>Big Blind: 40 chips • Small Blind: 20 chips • 6-Max Texas Hold'em</p>
        </footer>
      </div>
    </div>
  );
}