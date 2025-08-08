import psycopg2
from psycopg2.extras import RealDictCursor
from contextlib import contextmanager
from typing import Generator
from app.core.config import settings


class DatabaseManager:
    def __init__(self):
        self._connection = None
    
    def get_connection(self):
        if self._connection is None or self._connection.closed:
            self._connection = psycopg2.connect(
                host=settings.DB_HOST,
                port=settings.DB_PORT,
                user=settings.DB_USER,
                password=settings.DB_PASSWORD,
                database=settings.DB_NAME,
                cursor_factory=RealDictCursor
            )
        return self._connection
    
    @contextmanager
    def get_cursor(self) -> Generator:
        conn = self.get_connection()
        try:
            with conn.cursor() as cursor:
                yield cursor
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            conn.commit()
    
    def init_db(self):
        """Initialize database tables"""
        with self.get_cursor() as cursor:
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS hands (
                    id VARCHAR(36) PRIMARY KEY,
                    stacks INTEGER[],
                    dealer_index INTEGER,
                    small_blind_index INTEGER,
                    big_blind_index INTEGER,
                    actions TEXT[],
                    hole_cards TEXT[],
                    board TEXT,
                    winnings INTEGER[],
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)


db_manager = DatabaseManager()