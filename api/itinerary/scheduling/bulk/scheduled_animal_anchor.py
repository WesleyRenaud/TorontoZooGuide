from __future__ import annotations

from dataclasses import dataclass

from ...data_access.itinerary_animal_record import ItineraryAnimalRecord


@dataclass( frozen=True )
class ScheduledAnimalAnchor:
   animal: ItineraryAnimalRecord
   walk_node_id: str
   duration_seconds: int
