# Dockerfile.backend
FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy backend code
COPY . /app/

# Install Python dependencies directly
RUN pip install -r requirements.txt

# Set environment variables
ENV API_HOST=0.0.0.0
ENV API_PORT=8000
ENV FRONTEND_URL=http://frontend:3000

# Expose port
EXPOSE 8000

# Add healthcheck (commented out until health endpoint is implemented)
# HEALTHCHECK --interval=30s --timeout=10s --start-period=40s --retries=3 \
#   CMD curl -f http://localhost:8000/health || exit 1

# Run the application
CMD ["python", "-m", "app.main"]