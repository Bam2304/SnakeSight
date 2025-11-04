from typing import Any
import math, h3
from typing import Set

EARTH_RADIUS_KM = 6371.0088

def haversine_km(lat1: Any, lon1: Any, lat2: Any, lon2: Any) -> Any:
	"""TODO: Add description."""
	from math import radians, sin, cos, asin, sqrt
	dlat, dlon = radians(lat2-lat1), radians(lon2-lon1)
	a = sin(dlat/2)**2 + cos(radians(lat1))*cos(radians(lat2))*sin(dlon/2)**2
	return 2 * EARTH_RADIUS_KM * asin(sqrt(a))

def ring_for_radius_km(lat: Any, lon: Any, radius_km: Any, res: Any) -> Any:
	"""TODO: Add description."""
	edge_km = {5:3.6, 6:1.4, 7:0.55, 8:0.21, 9:0.08, 10:0.03}.get(res,0.21)
	k = max(1, int(math.ceil(radius_km / edge_km)))
	center = h3.geo_to_h3(lat, lon, res)
	cells = set(h3.k_ring(center, k))
	return {int(c) for c in cells}

def age_decay_score(age_days: Any, confidence: Any, distance_km: Any) -> Any:
	"""TODO: Add description."""
	lam = 0.08
	conf = confidence if confidence is not None else 0.7
	prox = 1.0 / (1.0 + (distance_km or 1.0))
	return conf * math.exp(-lam * age_days) * prox
