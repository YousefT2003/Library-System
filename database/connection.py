"""
Database Connection Module
Handles MySQL connection pooling and provides a reusable connection interface.
"""

import mysql.connector
from mysql.connector import pooling, Error
import os
from dotenv import load_dotenv

load_dotenv()  

# Database configuration — override via environment variables
DB_CONFIG = {
    'host': os.getenv('DB_HOST', 'localhost'),
    'port': int(os.getenv('DB_PORT', 3306)),
    'user': os.getenv('DB_USER', 'root'),
    'password': os.getenv('DB_PASSWORD'),
    'database': os.getenv('DB_NAME'),
}

# Connection pool for efficient resource usage
_pool = None


def get_pool():
    """Create or return the existing connection pool."""
    global _pool
    if _pool is None:
        try:
            _pool = pooling.MySQLConnectionPool(
                pool_name="library_pool",
                pool_size=10,
                pool_reset_session=True,
                **DB_CONFIG
            )
            print("[DB] Connection pool created successfully.")
        except Error as e:
            print(f"[DB] Error creating connection pool: {e}")
            raise
    return _pool


def get_connection():
    """Get a connection from the pool."""
    pool = get_pool()
    return pool.get_connection()


def execute_query(query, params=None, fetch=False, commit=False):
    """
    Execute a SQL query with optional parameters.
    
    Args:
        query: SQL query string
        params: Tuple of parameters for parameterized queries
        fetch: If True, return fetched rows
        commit: If True, commit the transaction
    
    Returns:
        Fetched rows (list of dicts) if fetch=True, else lastrowid or None
    """
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute(query, params or ())
        if fetch:
            result = cursor.fetchall()
            return result
        if commit:
            conn.commit()
            return cursor.lastrowid
        return None
    except Error as e:
        conn.rollback()
        raise e
    finally:
        cursor.close()
        conn.close()


def execute_many(query, data_list, commit=True):
    """Execute a query for multiple rows (batch insert/update)."""
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.executemany(query, data_list)
        if commit:
            conn.commit()
        return cursor.rowcount
    except Error as e:
        conn.rollback()
        raise e
    finally:
        cursor.close()
        conn.close()


def init_database():
    """
    Initialize the database by running schema.sql.
    Creates tables if they don't already exist.
    """
    import os
    schema_path = os.path.join(os.path.dirname(__file__), 'schema.sql')
    
    # First connect without database to create it if needed
    config_no_db = {k: v for k, v in DB_CONFIG.items() if k != 'database'}
    conn = mysql.connector.connect(**config_no_db)
    cursor = conn.cursor()
    try:
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS `{DB_CONFIG['database']}` "
                       f"CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci")
        conn.commit()
    finally:
        cursor.close()
        conn.close()

    # Now run schema
    conn = mysql.connector.connect(**DB_CONFIG)
    cursor = conn.cursor()
    try:
        with open(schema_path, 'r', encoding='utf-8') as f:
            sql = f.read()
        # Execute each statement individually
        for statement in sql.split(';'):
            stmt = statement.strip()
            if stmt:
                cursor.execute(stmt)
        conn.commit()
        print("[DB] Schema initialized successfully.")
    finally:
        cursor.close()
        conn.close()


def seed_database():
    """Run seed.sql to insert sample data."""
    import os
    seed_path = os.path.join(os.path.dirname(__file__), 'seed.sql')
    if not os.path.exists(seed_path):
        print("[DB] No seed.sql found, skipping.")
        return

    conn = mysql.connector.connect(**DB_CONFIG)
    cursor = conn.cursor()
    try:
        with open(seed_path, 'r', encoding='utf-8') as f:
            sql = f.read()
        for statement in sql.split(';'):
            stmt = statement.strip()
            if stmt:
                cursor.execute(stmt)
        conn.commit()
        print("[DB] Seed data inserted successfully.")
    except Error as e:
        conn.rollback()
        print(f"[DB] Seed error (may already exist): {e}")
    finally:
        cursor.close()
        conn.close()
    
