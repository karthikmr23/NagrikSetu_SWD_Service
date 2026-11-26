import pytest
from app.database.connection import SessionLocal
from app.models import DynamicFormDefinition, DynamicFormField, Scheme, SchemeApplication, SchemeCategory
from sqlalchemy import select

def test_dynamic_forms_seed_and_coverage():
    """Verify schemes have dynamic form definitions in MySQL."""
    db = SessionLocal()
    try:
        schemes = db.query(Scheme).all()
        assert len(schemes) >= 35, f"Expected at least 35 schemes, found {len(schemes)}"
        
        forms = db.query(DynamicFormDefinition).all()
        assert len(forms) >= 35, f"Expected at least 35 dynamic form definitions, found {len(forms)}"
        
        # Verify fields exist
        fields = db.query(DynamicFormField).all()
        assert len(fields) >= 100, f"Expected >= 100 dynamic fields across schemes, found {len(fields)}"
    finally:
        db.close()

def test_automatic_category_routing_on_application():
    """Verify that scheme applications automatically inherit category_id from the scheme."""
    db = SessionLocal()
    try:
        # Check all applications have category_id populated
        apps = db.query(SchemeApplication).all()
        assert len(apps) > 0, "No applications found"
        for app in apps:
            assert app.category_id is not None, f"Application {app.id} has null category_id"
            # Verify category matches scheme category
            scheme = db.get(Scheme, app.scheme_id)
            assert app.category_id == scheme.category_id, f"Application category {app.category_id} != scheme category {scheme.category_id}"
    finally:
        db.close()

def test_portal_category_stats_endpoint():
    """Verify category stats endpoint returns live counts and breakdown."""
    from fastapi.testclient import TestClient
    from app.main import app
    from app.core.security import create_access_token
    
    client = TestClient(app)
    admin_token = create_access_token({"sub": "ADM-001", "role": "SWD_ADMIN", "email": "swd.admin@nagriksetu.local"})
    headers = {"Authorization": f"Bearer {admin_token}"}
    
    res = client.get("/api/swd/admin/categories/stats", headers=headers)
    assert res.status_code == 200
    data = res.json()
    assert len(data) >= 8, f"Expected >= 8 categories, got {len(data)}"
    
    first_cat = data[0]
    assert "category_id" in first_cat
    assert "category_name" in first_cat
    assert "total_applications" in first_cat
    assert "schemes" in first_cat
    assert isinstance(first_cat["schemes"], list)
