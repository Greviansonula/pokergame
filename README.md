# Poker Game API

A Texas Hold'em Poker Game API built with FastAPI and PostgreSQL.

## Environment Setup

### 1. Create Environment File

Copy the example environment file and configure your secrets:

```bash
cp env.example .env
```

### 2. Configure Environment Variables

Edit the `.env` file with your actual values:

```env
# Database Configuration
DB_HOST=localhost
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

### 3. Security Notes

- **Never commit your `.env` file** to version control
- Use strong, unique passwords for database credentials
- Consider using a secrets management service for production

## Running the Application

### Using Docker Compose

```bash
docker-compose up -d
```

### Running Backend Locally

```bash
cd backend
pip install -r requirements.txt
python -m app.main
```

## API Endpoints

- `POST /api/v1/hands/` - Create a new poker hand
- `GET /api/v1/hands/` - Get all poker hands
- `GET /api/v1/hands/{hand_id}` - Get a specific poker hand

## Development

The application uses environment variables for configuration. The `env.example` file contains all required variables with placeholder values.
