def test_neural_vault_logging_persistence():
    """
    Verifies that the MariaDB instance at 10.10.12.15 logs the 
    schematic generation event for CoreProtect-style rollback support.
    """
    event_id = "VOID_TECH_MUTATION_087"
    vault_status = neural_vault.log_build_event(event_id, timestamp="2026-04-01")
    
    # Ensure event is queryable for future rollbacks
    logged_event = neural_vault.query_event(event_id)
    assert logged_event["id"] == event_id
    assert logged_event["db_type"] == "sql"
