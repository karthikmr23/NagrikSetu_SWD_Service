import pytest
import requests

BASE_URL = "http://127.0.0.1:8004"

def test_gps_offices_nearby_bengaluru():
    """Test GPS search near Vidhana Soudha, Bengaluru within 25 km against live service."""
    # Vidhana Soudha coords: 12.9791, 77.5913
    response = requests.get(f"{BASE_URL}/api/swd/offices/nearby?latitude=12.9791&longitude=77.5913&radius_km=25")
    assert response.status_code == 200
    data = response.json()
    assert len(data) >= 3, f"Expected at least 3 offices in Bengaluru area, got {len(data)}"
    
    # Check that results are sorted ascending by distance
    distances = [item["distance_km"] for item in data]
    assert distances == sorted(distances), "Results must be sorted nearest-to-farthest"
    
    # Check that all distances are strictly <= 25.0 km
    for item in data:
        assert item["distance_km"] <= 25.0
        assert item["is_active"] is True
        assert item["verification_status"] == "VERIFIED"

def test_gps_offices_nearby_empty_state():
    """Test GPS search at coordinates far away (e.g. New Delhi), ensuring empty list returned."""
    # New Delhi coords: 28.6139, 77.2090
    response = requests.get(f"{BASE_URL}/api/swd/offices/nearby?latitude=28.6139&longitude=77.2090&radius_km=25")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 0, f"Expected 0 offices within 25 km of New Delhi, got {len(data)}"

def test_gps_offices_nearby_radius_enforcement():
    """Test that radius parameter cannot exceed 25 km and raises validation error if over 25.0."""
    response = requests.get(f"{BASE_URL}/api/swd/offices/nearby?latitude=12.9791&longitude=77.5913&radius_km=100")
    # Pydantic Query(le=25.0) validates and strictly rejects > 25.0 with 422 Unprocessable Entity
    assert response.status_code == 422, "Strict 25 km limit must reject requests asking for > 25 km"
    
    # Within 25.0 km must succeed
    response_valid = requests.get(f"{BASE_URL}/api/swd/offices/nearby?latitude=12.9791&longitude=77.5913&radius_km=25.0")
    assert response_valid.status_code == 200
    for item in response_valid.json():
        assert item["distance_km"] <= 25.0
