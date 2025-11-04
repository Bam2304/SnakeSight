from typing import Any
from fastapi import APIRouter, Depends, Header, HTTPException, Query
from sqlalchemy.orm import Session
from typing import Optional
from ..db import get_db
from ..schemas import SightingCreate, SightingOut, LastKnownResponse, MySightingsResponse
from .. import crud
from ..config import settings

router = APIRouter(prefix="/api", tags=["sightings"])

def require_user(x_user_id: Optional[str]) -> Any:
	"""TODO: Add description."""
	if not x_user_id:
		raise HTTPException(status_code=401, detail="Missing X-User-Id header")
	return x_user_id

@router.post("/sightings", response_model=SightingOut)
def post_sighting(payload: SightingCreate, db: Session = Depends(get_db), x_user_id: Optional[str] = Header(None, convert_underscores=False)) -> Any:
	"""TODO: Add description."""
	user_id = require_user(x_user_id)
	s = crud.create_sighting(db, user_id=user_id, payload=payload)
	return s.__dict__

@router.get("/last-known", response_model=LastKnownResponse)
def get_last_known(lat: float = Query(...), lon: float = Query(...),
				   radius_km: float = Query(settings.DEFAULT_RADIUS_KM, ge=0.1, le=200.0),
				   since_days: int = Query(settings.DEFAULT_SINCE_DAYS, ge=1, le=3650),
				   venom_only: bool = Query(False), db: Session = Depends(get_db)):
	results = crud.last_known_by_point(db, lat=lat, lon=lon, radius_km=radius_km, since_days=since_days, venom_only=venom_only)
	return {"results": results}

@router.get("/me/sightings", response_model=MySightingsResponse)
def get_my_sightings(since_days: int = Query(365, ge=1, le=3650), db: Session = Depends(get_db), x_user_id: Optional[str] = Header(None, convert_underscores=False)) -> Any:
	"""TODO: Add description."""
	user_id = require_user(x_user_id)
	items = crud.list_my_sightings(db, user_id=user_id, since_days=since_days)
	return {"items": [s.__dict__ for s in items]}
