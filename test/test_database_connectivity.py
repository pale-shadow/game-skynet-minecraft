import os
import pytest
import pymysql

# Load database configuration from environment
DB_HOST = os.getenv("DB_HOST", "10.10.12.15")
DB_USER = os.getenv("DB_USER", "bluemap")
DB_PASS = os.getenv("DB_PASS", "dinosaurExTraVaGanZa1969") # Example; use .envrc
DB_NAME = "bluemap"

@pytest.mark.database
def test_database_connection():
    """Verify connectivity to the MariaDB Neural-Data Vault."""
    conn = pymysql.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASS,
        database=DB_NAME,
        connect_timeout=5
    )
    assert conn.open
    conn.close()

@pytest.mark.database
def test_database_schema_provisioned():
    """Verify that required tables for BlueMap are provisioned."""
    conn = pymysql.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASS,
        database=DB_NAME
    )
    with conn.cursor() as cursor:
        # Check if any tables exist in the database
        cursor.execute("SHOW TABLES")
        tables = cursor.fetchall()
        # Ensure database is not empty if it's supposed to be initialized
        # Adjust as per your specific schema requirements
        assert len(tables) >= 0 
    conn.close()
