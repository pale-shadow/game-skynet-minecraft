import os

import pymysql
import pytest

# Load database configuration from environment or use discovered defaults
DB_HOST = os.getenv("DB_HOST", "10.10.12.15")
DB_PASS = os.getenv("DB_PASS", "dinosaur")  # Historical placeholder from setup.sql

DATABASES = [
    {"name": "bluemap", "user": "bluemap"},
    {"name": "luckperms", "user": "luckperms"},
    {"name": "coreprotect", "user": "coreprotect"},
    {"name": "skynet_vault", "user": "skynet_admin"},
]


@pytest.mark.database
@pytest.mark.parametrize("db_info", DATABASES)
def test_vault_multi_db_connectivity(db_info):
    """Verify connectivity to all specialized schemas on Hub 07."""
    try:
        conn = pymysql.connect(
            host=DB_HOST,
            user=db_info["user"],
            password=DB_PASS,
            database=db_info["name"],
            connect_timeout=3,
        )
        assert conn.open
        conn.close()
    except pymysql.Error as e:
        pytest.fail(
            f"Connectivity failure for {db_info['name']} as {db_info['user']}: {e}"
        )


@pytest.mark.database
def test_skynet_vault_schema_integrity():
    """Validate that the skynet_vault has the required urbanization telemetry columns."""
    conn = pymysql.connect(
        host=DB_HOST, user="skynet_admin", password=DB_PASS, database="skynet_vault"
    )
    with conn.cursor() as cursor:
        cursor.execute("DESCRIBE build_history")
        columns = [col[0] for col in cursor.fetchall()]

        required_columns = [
            "id",
            "name",
            "x",
            "y",
            "z",
            "width",
            "depth",
            "schematic_name",
            "ai_hardware",
            "timestamp",
        ]

        for req in required_columns:
            assert (
                req in columns
            ), f"Missing mandatory column '{req}' in skynet_vault.build_history"

    conn.close()


@pytest.mark.database
def test_vault_permissions_audit():
    """Ensure service users cannot access unauthorized schemas."""
    # Test that 'bluemap' user cannot access 'skynet_vault'
    with pytest.raises(pymysql.Error):
        pymysql.connect(
            host=DB_HOST,
            user="bluemap",
            password=DB_PASS,
            database="skynet_vault",
            connect_timeout=3,
        )
