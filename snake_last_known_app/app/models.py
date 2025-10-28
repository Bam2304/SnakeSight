from sqlalchemy import Column, String, Float, Text, DateTime, Enum, Index
from sqlalchemy.types import BIGINT
from sqlalchemy.orm import mapped_column, Mapped
from datetime import datetime
import enum, uuid
from .db import Base

def UUIDColumn():
    return mapped_column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))

class VenomStatus(str, enum.Enum):
    venomous = "venomous"
    non_venomous = "non_venomous"
    unknown = "unknown"

class SightingStatus(str, enum.Enum):
    active = "active"
    flagged = "flagged"
    removed = "removed"

class Sighting(Base):
    __tablename__ = "snake_sightings"
    id: Mapped[str] = UUIDColumn()
    user_id: Mapped[str] = mapped_column(String(64), index=True, nullable=False)
    species_text: Mapped[str] = mapped_column(String(120), nullable=False)
    venom_status: Mapped[VenomStatus] = mapped_column(Enum(VenomStatus), default=VenomStatus.unknown, nullable=False)
    lat: Mapped[float] = mapped_column(Float, nullable=False)
    lon: Mapped[float] = mapped_column(Float, nullable=False)
    h3_index: Mapped[int | None] = mapped_column(BIGINT, index=True)
    observed_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, index=True)
    visibility: Mapped[str] = mapped_column(String(10), default="public", index=True)
    confidence: Mapped[float | None] = mapped_column(Float, nullable=True)
    photo_url: Mapped[str | None] = mapped_column(Text, nullable=True)
    note: Mapped[str | None] = mapped_column(Text, nullable=True)
    status: Mapped[SightingStatus] = mapped_column(Enum(SightingStatus), default=SightingStatus.active, index=True)
Index("idx_species_h3", Sighting.species_text, Sighting.h3_index)
