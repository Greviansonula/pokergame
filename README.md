# Texas Hold'em Poker Game

A full-stack Texas Hold'em poker game with real-time gameplay, hand history tracking, and a modern web interface.

## Features

- 🎮 6-player Texas Hold'em gameplay
- 📊 Real-time hand history and statistics
- 🎯 Interactive betting controls
- 💾 Persistent game data storage
- 🐳 Docker containerization
- 🔄 RESTful API backend

## Preview
<img width="959" height="514" alt="Screenshot 2025-08-12 224518" src="https://github.com/user-attachments/assets/09aa174e-d8af-4e20-9b57-3c58ec58202f" />

## Tech Stack

- **Backend**: FastAPI, PostgreSQL
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

2. **Set up environment variables**
   
   Create a `.env` file in the project root with the following contents:
   ```bash
   # Copy the environment configuration from:
   # https://privatebin.net/?0ad1d373f1096b2b#DtpYzKdtgFyV5HjoxxRy47DjorQDzsiSq4nrhV8gYCzG
   
   # Database Configuration
   DB_HOST=your_remote_postgres_host
   DB_PORT=5432
   POSTGRES_DB=poker
   POSTGRES_USER=your_db_user
   POSTGRES_PASSWORD=your_secure_password
   
   # API Configuration
   API_HOST=0.0.0.0
   API_PORT=8000
   
   # CORS Configuration
   FRONTEND_URL=http://localhost:3000
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
python3.12 -m venv .venv
source .venv/bin/activate
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
```
pokergame/
├── .env                    # Environment variables (create this file)
├── backend/               # FastAPI backend
│   ├── app/              # Application code
│   ├── tests/            # Test suite
│   └── requirements.txt
├── frontend/             # Next.js frontend
│   ├── components/       # React components
│   ├── store/            # State management
│   └── package.json
└── docker-compose.yml
```

## Environment Configuration

The application requires environment variables to be configured in a `.env` file at the project root. This file contains:

- **Database credentials** for your PostgreSQL instance
- **API configuration** for the backend service
- **CORS settings** for frontend-backend communication


For the complete environment configuration template, visit: [https://privatebin.net/?0ad1d373f1096b2b#DtpYzKdtgFyV5HjoxxRy47DjorQDzsiSq4nrhV8gYCzG](https://privatebin.net/?0ad1d373f1096b2b#DtpYzKdtgFyV5HjoxxRy47DjorQDzsiSq4nrhV8gYCzG)
