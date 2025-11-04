from typing import Any
from pydantic import BaseModel, field_validator
from typing import Optional
from datetime import datetime
from enum import Enum

class VenomStatus(str, Enum):
	venomous = "venomous"
	non_venomous = "non_venomous"
	unknown = "unknown"

class SightingCreate(BaseModel):
	species_text: str
	lat: float
	lon: float
	venom_status: VenomStatus = VenomStatus.unknown
	visibility: str = "public"
	confidence: Optional[float] = None
	photo_url: Optional[str] = None
	note: Optional[str] = None

	@field_validator("visibility")
	def check_visibility(cls: Any, v: Any) -> Any:
		"""TODO: Add description."""
		if v not in ("public", "private"):
			raise ValueError("visibility must be 'public' or 'private'")
		return v

class SightingOut(BaseModel):
	id: str
	user_id: str
	species_text: str
	venom_status: VenomStatus
	lat: float
	lon: float
	h3_index: int | None
	observed_at: datetime
	visibility: str
	confidence: float | None
	photo_url: str | None
	note: str | None
	status: str

class LastKnownItem(BaseModel):
	species_text: str
	last_seen_at: datetime
	nearest_distance_km: float | None
	count_30d: int
	score: float

class LastKnownResponse(BaseModel):
	results: list[LastKnownItem]

class MySightingsResponse(BaseModel):
	items: list[SightingOut]
