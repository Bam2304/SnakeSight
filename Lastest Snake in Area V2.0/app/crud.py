from typing import Any
from sqlalchemy.orm import Session
from sqlalchemy import select, desc
from datetime import datetime, timedelta
from .models import Sighting, SightingStatus
from .schemas import SightingCreate
from .config import settings
from . import utils_geo
import h3

def create_sighting(db: Session, *, user_id: str, payload: SightingCreate) -> Any:
	"""TODO: Add description."""
	h3_idx = int(h3.geo_to_h3(payload.lat, payload.lon, settings.H3_RESOLUTION))
	s = Sighting(user_id=user_id, species_text=payload.species_text.strip(),
				 venom_status=payload.venom_status.value, lat=payload.lat, lon=payload.lon,
				 h3_index=h3_idx, observed_at=datetime.utcnow(), visibility=payload.visibility,
				 confidence=payload.confidence, photo_url=payload.photo_url, note=payload.note,
				 status=SightingStatus.active)
	db.add(s)
	db.commit(); db.refresh(s)
	return s

def list_my_sightings(db: Session, *, user_id: str, since_days: int = 365) -> Any:
	"""TODO: Add description."""
	since_dt = datetime.utcnow() - timedelta(days=since_days)
	q = select(Sighting).where(Sighting.user_id==user_id, Sighting.observed_at>=since_dt,
							   Sighting.status==SightingStatus.active).order_by(desc(Sighting.observed_at))
	return list(db.scalars(q).all())

def last_known_by_point(db: Session, *, lat: Any, lon: Any, radius_km: Any, since_days: Any, venom_only: Any) -> Any:
	"""TODO: Add description."""
	cells = utils_geo.ring_for_radius_km(lat, lon, radius_km, settings.H3_RESOLUTION)
	since_dt = datetime.utcnow() - timedelta(days=since_days)
	last30 = datetime.utcnow() - timedelta(days=30)
	q = select(Sighting).where(Sighting.h3_index.in_(cells), Sighting.status==SightingStatus.active,
							   Sighting.visibility=='public', Sighting.observed_at>=since_dt)
	if venom_only:
		q = q.where(Sighting.venom_status=='venomous')
	rows = list(db.scalars(q).all())
	if not rows: return []
	by_species = {}
	for r in rows: by_species.setdefault(r.species_text, []).append(r)
	now = datetime.utcnow(); out = []
	for species, items in by_species.items():
		last_seen = max(items, key=lambda r: r.observed_at).observed_at
		count_30d = sum(1 for r in items if r.observed_at >= last30)
		nearest_km = min(utils_geo.haversine_km(lat, lon, r.lat, r.lon) for r in items)
		best = max(items, key=lambda r: (r.confidence or 0.0, r.observed_at))
		age_days = (now - best.observed_at).total_seconds()/86400.0
		score = utils_geo.age_decay_score(age_days, best.confidence, nearest_km)
		out.append({'species_text':species,'last_seen_at':last_seen,'nearest_distance_km':round(nearest_km,3),
					'count_30d':count_30d,'score':round(score,6)})
	out.sort(key=lambda x:(x['score'],x['last_seen_at']), reverse=True)
	return out
