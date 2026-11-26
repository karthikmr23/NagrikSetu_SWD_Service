import math
from typing import List, Optional
from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from pydantic import BaseModel, ConfigDict, Field

from app.database.connection import get_db
from app.models import Office
from app.core.security import require_role

router = APIRouter(prefix="/api/swd", tags=["SWD Office Locator"])

def haversine_distance_km(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """
    Computes great-circle distance between two GPS points using the Haversine formula.
    Returns distance in kilometres rounded to two decimal places.
    """
    R = 6371.0 # Earth's radius in kilometres
    phi1 = math.radians(lat1)
    phi2 = math.radians(lat2)
    delta_phi = math.radians(lat2 - lat1)
    delta_lambda = math.radians(lon2 - lon1)

    a = (math.sin(delta_phi / 2.0) ** 2 +
         math.cos(phi1) * math.cos(phi2) * (math.sin(delta_lambda / 2.0) ** 2))
    c = 2.0 * math.atan2(math.sqrt(a), math.sqrt(1.0 - a))
    return round(R * c, 2)

class OfficeBase(BaseModel):
    name: str
    office_type: str = "District Welfare Office"
    district: str
    taluk: Optional[str] = None
    address: str
    contact_number: Optional[str] = None
    email: Optional[str] = None
    working_hours: Optional[str] = "10:00 AM - 5:30 PM (Mon-Sat)"
    services_offered: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    map_link: Optional[str] = None
    is_active: bool = True
    verification_status: str = "VERIFIED"

class OfficeCreate(OfficeBase):
    pass

class OfficeUpdate(BaseModel):
    name: Optional[str] = None
    office_type: Optional[str] = None
    district: Optional[str] = None
    taluk: Optional[str] = None
    address: Optional[str] = None
    contact_number: Optional[str] = None
    email: Optional[str] = None
    working_hours: Optional[str] = None
    services_offered: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    map_link: Optional[str] = None
    is_active: Optional[bool] = None
    verification_status: Optional[str] = None

class OfficeResponse(OfficeBase):
    id: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)

class NearbyOfficeResponse(OfficeResponse):
    distance_km: float

# ----------------- GPS Nearby Welfare Centre Search -----------------

@router.get("/offices/nearby", response_model=List[NearbyOfficeResponse])
def get_nearby_offices(
    latitude: float = Query(..., ge=-90.0, le=90.0, description="Citizen current GPS latitude"),
    longitude: float = Query(..., ge=-180.0, le=180.0, description="Citizen current GPS longitude"),
    radius_km: float = Query(25.0, ge=1.0, le=25.0, description="Search radius in kilometres (strictly capped at 25 km)"),
    db: Session = Depends(get_db)
):
    """
    Finds active and verified Social Welfare Department centres within exactly 25 km of the citizen GPS coordinates.
    Calculates distances using the Haversine formula and returns results sorted from nearest to farthest.
    """
    # Enforce strict maximum radius constraint of exactly 25.0 km
    search_radius = min(float(radius_km), 25.0)

    # Fetch ONLY active and verified offices that have valid GPS coordinates
    offices = db.query(Office).filter(
        Office.is_active == True,
        Office.verification_status == "VERIFIED",
        Office.latitude.isnot(None),
        Office.longitude.isnot(None)
    ).all()

    nearby_results: List[NearbyOfficeResponse] = []

    for off in offices:
        if off.latitude is None or off.longitude is None:
            continue

        dist = haversine_distance_km(latitude, longitude, float(off.latitude), float(off.longitude))

        # Strict boundary rule: include only if distance is <= 25.0 km
        if dist <= search_radius:
            office_dict = {
                "id": off.id,
                "name": off.name,
                "office_type": off.office_type,
                "district": off.district,
                "taluk": off.taluk,
                "address": off.address,
                "contact_number": off.contact_number,
                "email": off.email,
                "working_hours": off.working_hours,
                "services_offered": off.services_offered,
                "latitude": float(off.latitude) if off.latitude else None,
                "longitude": float(off.longitude) if off.longitude else None,
                "map_link": off.map_link,
                "is_active": off.is_active,
                "verification_status": off.verification_status,
                "created_at": off.created_at,
                "updated_at": off.updated_at,
                "distance_km": dist
            }
            nearby_results.append(NearbyOfficeResponse(**office_dict))

    # Sort strictly from nearest to farthest
    nearby_results.sort(key=lambda x: x.distance_km)

    return nearby_results

# ----------------- Standard Manual Search & Management Endpoints -----------------

@router.get("/offices", response_model=List[OfficeResponse])
def list_offices(
    district: Optional[str] = None,
    taluk: Optional[str] = None,
    office_type: Optional[str] = None,
    search: Optional[str] = None,
    is_active: Optional[bool] = True,
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=200),
    db: Session = Depends(get_db)
):
    query = db.query(Office)
    if is_active is not None:
        query = query.filter(Office.is_active == is_active)
    if district and district.strip() and district.upper() != "ALL":
        query = query.filter(Office.district.ilike(f"%{district.strip()}%"))
    if taluk and taluk.strip() and taluk.upper() != "ALL":
        query = query.filter(Office.taluk.ilike(f"%{taluk.strip()}%"))
    if office_type and office_type.strip() and office_type.upper() != "ALL":
        query = query.filter(Office.office_type.ilike(f"%{office_type.strip()}%"))
    if search and search.strip():
        s = f"%{search.strip()}%"
        query = query.filter((Office.name.ilike(s)) | (Office.address.ilike(s)) | (Office.services_offered.ilike(s)))
    return query.order_by(Office.district.asc(), Office.name.asc()).offset(skip).limit(limit).all()

@router.get("/offices/{office_id}", response_model=OfficeResponse)
def get_office(office_id: int, db: Session = Depends(get_db)):
    off = db.query(Office).filter(Office.id == office_id).first()
    if not off:
        raise HTTPException(status_code=404, detail="Welfare office not found")
    return off

@router.post("/offices", response_model=OfficeResponse)
def create_office(
    office_in: OfficeCreate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(require_role(["ADMINISTRATOR", "SWD_ADMIN"]))
):
    new_off = Office(**office_in.model_dump())
    db.add(new_off)
    db.commit()
    db.refresh(new_off)
    return new_off

@router.put("/offices/{office_id}", response_model=OfficeResponse)
def update_office(
    office_id: int,
    office_in: OfficeUpdate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(require_role(["ADMINISTRATOR", "SWD_ADMIN"]))
):
    off = db.query(Office).filter(Office.id == office_id).first()
    if not off:
        raise HTTPException(status_code=404, detail="Welfare office not found")
    for field, val in office_in.model_dump(exclude_unset=True).items():
        setattr(off, field, val)
    db.commit()
    db.refresh(off)
    return off

@router.delete("/offices/{office_id}")
def deactivate_office(
    office_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(require_role(["ADMINISTRATOR", "SWD_ADMIN"]))
):
    off = db.query(Office).filter(Office.id == office_id).first()
    if not off:
        raise HTTPException(status_code=404, detail="Welfare office not found")
    off.is_active = False
    db.commit()
    return {"message": f"Office '{off.name}' deactivated successfully."}
