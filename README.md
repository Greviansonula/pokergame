# Texas Hold'em Poker Game

A full-stack Texas Hold'em poker game with real-time gameplay, hand history tracking, and a modern web interface.

## Features

- 🎮 6-player Texas Hold'em gameplay
- 📊 Real-time hand history and statistics
- 🎯 Interactive betting controls
- 💾 Persistent game data storage
- 🐳 Docker containerization
- 🔄 RESTful API backend

## Tech Stack

- **Backend**: FastAPI, PostgreSQL, SQLAlchemy
- **Frontend**: Next.js, TypeScript, Tailwind CSS
- **State Management**: Zustand
- **Database**: PostgreSQL with Alembic migrations
- **Containerization**: Docker & Docker Compose

## Prerequisites

- Docker Desktop
- Node.js 18+ (for local development)
- Python 3.8+ (for local development)

## Quick Start

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd pokergame
   ```

2. **Set up environment**
   ```bash
   cp backend/env.example backend/.env
   # Edit backend/.env with your database credentials
   ```

3. **Start the application**
   ```bash
   docker compose up -d
   ```

4. **Access the game**
   - Frontend: http://localhost:3000
   - Backend API: http://localhost:8000
   - API Docs: http://localhost:8000/docs

## Game Instructions

1. **Set up players** with starting chip stacks
2. **Start a hand** to begin gameplay
3. **Play through phases**: Preflop → Flop → Turn → River → Showdown
4. **View hand history** in the right panel
5. **Track statistics** and replay previous hands

## API Documentation

### Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/api/v1/hands/` | Create a new poker hand |
| `GET` | `/api/v1/hands/` | Get all poker hands |
| `GET` | `/api/v1/hands/{id}` | Get a specific poker hand |

### Example Request

```json
POST /api/v1/hands/
{
  "stacks": [1000, 1000, 1000, 1000, 1000, 1000],
  "dealer_index": 0,
  "small_blind_index": 1,
  "big_blind_index": 2,
  "actions": ["Player 1 calls 40", "Player 2 folds"],
  "hole_cards": ["AsKs", "QdJd", "", "", "", ""],
  "board": "AhKhQc"
}
```

## Development

### Local Development Setup

```bash
# Backend
cd backend
pip install -r requirements.txt
python -m app.main

# Frontend
cd frontend
npm install
npm run dev
```

### Testing

```bash
# Backend tests
cd backend
pytest
```

### Project Structure
pokergame/
├── backend/ # FastAPI backend
│ ├── app/ # Application code
│ ├── tests/ # Test suite
│ └── requirements.txt
├── frontend/ # Next.js frontend
│ ├── components/ # React components
│ ├── store/ # State management
│ └── package.json
└── docker-compose.yml