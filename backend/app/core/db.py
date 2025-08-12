import psycopg2
from psycopg2.extras import RealDictCursor
from contextlib import contextmanager
from typing import Generator

class DatabaseManager:
    def __init__(self):
        self._connection = None

        # Hardcoded DB credentials
        self.DB_HOST = "ls-6a894f612a8456af893817405d629367d4e9764a.cfgusgase70s.ap-south-1.rds.amazonaws.com"
        self.DB_PORT = 5432
        self.DB_USER = "dbmasteruser"
        self.DB_PASSWORD = "4>pQxt6_,&HGGXQ(k9t.(A#hhK.fwSBS"
        self.DB_NAME = "pokerdb"

        print("Using DB connection:")
        print(f"HOST: {self.DB_HOST}")
        print(f"PORT: {self.DB_PORT}")
        print(f"USER: {self.DB_USER}")
        print(f"NAME: {self.DB_NAME}")
    
    def get_connection(self):
        if self._connection is None or self._connection.closed:
            self._connection = psycopg2.connect(
                host=self.DB_HOST,
                port=self.DB_PORT,
                user=self.DB_USER,
                password=self.DB_PASSWORD,
                database=self.DB_NAME,
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
