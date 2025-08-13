import psycopg2
from psycopg2.extras import RealDictCursor
from psycopg2.pool import SimpleConnectionPool
from contextlib import contextmanager
from typing import Generator
import os
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class DatabaseManager:
    def __init__(self):
        # Hardcoded DB credentials
        self.DB_HOST = "ls-6a894f612a8456af893817405d629367d4e9764a.cfgusgase70s.ap-south-1.rds.amazonaws.com"
        self.DB_PORT = 5432
        self.DB_USER = "dbmasteruser"
        self.DB_PASSWORD = "4>pQxt6_,&HGGXQ(k9t.(A#hhK.fwSBS"
        self.DB_NAME = "pokerdb"
        
        # Create a connection pool
        self._pool = None
        self._init_pool()
        
        logger.info("Database manager initialized")
        logger.info(f"DB_HOST: {self.DB_HOST}")
        logger.info(f"DB_PORT: {self.DB_PORT}")
        logger.info(f"DB_USER: {self.DB_USER}")
        logger.info(f"DB_NAME: {self.DB_NAME}")
    
    def _init_pool(self):
        """Initialize the connection pool"""
        try:
            self._pool = SimpleConnectionPool(
                minconn=1,
                maxconn=10,
                host=self.DB_HOST,
                port=self.DB_PORT,
                user=self.DB_USER,
                password=self.DB_PASSWORD,
                database=self.DB_NAME,
                cursor_factory=RealDictCursor
            )
            logger.info("Database connection pool initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize connection pool: {e}")
            logger.exception("Connection pool initialization error details:")
            self._pool = None
    
    def get_connection(self):
        """Get a connection from the pool"""
        if self._pool is None:
            logger.warning("Connection pool is None, attempting to reinitialize")
            self._init_pool()
        
        try:
            conn = self._pool.getconn()
            # Test if connection is still alive using a simple query instead of ping()
            try:
                with conn.cursor() as cursor:
                    cursor.execute("SELECT 1")
                    cursor.fetchone()
                logger.debug("Successfully obtained connection from pool")
                return conn
            except Exception as ping_error:
                logger.warning(f"Connection test failed, closing and getting new connection: {ping_error}")
                try:
                    conn.close()
                except:
                    pass
                # Get a fresh connection
                conn = self._pool.getconn()
                logger.debug("Successfully obtained fresh connection from pool")
                return conn
        except Exception as e:
            logger.error(f"Error getting connection from pool: {e}")
            logger.exception("Connection error details:")
            # Try to reinitialize pool
            logger.info("Attempting to reinitialize connection pool")
            self._init_pool()
            if self._pool:
                try:
                    return self._pool.getconn()
                except Exception as retry_e:
                    logger.error(f"Failed to get connection after pool reinitialization: {retry_e}")
                    logger.exception("Retry connection error details:")
                    raise retry_e
            raise e
    
    def return_connection(self, conn):
        """Return a connection to the pool"""
        if self._pool and conn:
            try:
                self._pool.putconn(conn)
                logger.debug("Successfully returned connection to pool")
            except Exception as e:
                logger.error(f"Error returning connection to pool: {e}")
                logger.exception("Connection return error details:")
                try:
                    conn.close()
                    logger.info("Closed problematic connection")
                except Exception as close_e:
                    logger.error(f"Error closing problematic connection: {close_e}")
        else:
            logger.warning("Cannot return connection: pool is None or connection is None")
    
    @contextmanager
    def get_cursor(self) -> Generator:
        conn = None
        try:
            logger.debug("Getting database cursor")
            conn = self.get_connection()
            with conn.cursor() as cursor:
                logger.debug("Database cursor obtained successfully")
                yield cursor
                conn.commit()
                logger.debug("Database transaction committed successfully")
        except Exception as e:
            logger.error(f"Database cursor error: {e}")
            logger.exception("Database cursor error details:")
            if conn:
                try:
                    conn.rollback()
                    logger.info("Database transaction rolled back")
                except Exception as rollback_e:
                    logger.error(f"Error during rollback: {rollback_e}")
            raise e
        finally:
            if conn:
                self.return_connection(conn)
    
    def init_db(self):
        """Initialize database tables"""
        logger.info("Initializing database tables")
        try:
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
                logger.info("Database tables initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize database tables: {e}")
            logger.exception("Database initialization error details:")
            raise e
    
    def close_pool(self):
        """Close all connections in the pool"""
        if self._pool:
            try:
                self._pool.closeall()
                logger.info("Database connection pool closed successfully")
            except Exception as e:
                logger.error(f"Error closing connection pool: {e}")
                logger.exception("Pool closure error details:")

db_manager = DatabaseManager()
