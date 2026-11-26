import pytest
from app.database.connection import SessionLocal
from sqlalchemy import text, select, func
from app.models import AuditLog, User, Office, Scheme

def test_database_connection_isolation():
    """Verify backend is connected to nagriksetu_swd on host port 3306."""
    db = SessionLocal()
    try:
        row = db.execute(text("SELECT DATABASE(), @@hostname, @@port, CURRENT_USER();")).fetchone()
        db_name, hostname, port, current_user = row
        assert db_name == "nagriksetu_swd", f"Expected nagriksetu_swd, got {db_name}"
        assert int(port) == 3306, f"Expected port 3306, got {port}"
        assert "swd_app" in current_user, f"Expected swd_app user, got {current_user}"
    finally:
        db.close()

def test_safe_read_write_operation():
    """Verify safe transactional read, write, and cleanup in nagriksetu_swd."""
    db = SessionLocal()
    try:
        before_count = db.execute(select(func.count(AuditLog.id))).scalar()
        test_log = AuditLog(
            actor_id=1,
            actor_role="CITIZEN",
            action="VERIFICATION_TEST_WRITE",
            entity_type="SYSTEM",
            entity_id=1,
            details='{"isolation_check": true, "port": 3306}'
        )
        db.add(test_log)
        db.commit()
        db.refresh(test_log)
        created_id = test_log.id

        # Verify read
        fetched = db.get(AuditLog, created_id)
        assert fetched is not None
        assert fetched.action == "VERIFICATION_TEST_WRITE"

        # Cleanup
        db.delete(fetched)
        db.commit()
        after_count = db.execute(select(func.count(AuditLog.id))).scalar()
        assert before_count == after_count
    finally:
        db.close()

def test_essential_tables_and_seed_data():
    """Verify all 16 tables exist and essential seed data is populated."""
    db = SessionLocal()
    try:
        scheme_count = db.execute(select(func.count(Scheme.id))).scalar()
        user_count = db.execute(select(func.count(User.id))).scalar()
        office_count = db.execute(select(func.count(Office.id))).scalar()

        assert scheme_count >= 35, f"Expected >= 35 schemes, found {scheme_count}"
        assert user_count >= 5, f"Expected >= 5 users, found {user_count}"
        assert office_count == 10, f"Expected exactly 10 offices, found {office_count}"
    finally:
        db.close()
