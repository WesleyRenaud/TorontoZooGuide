from __future__ import annotations

from dataclasses import dataclass

from ...data_access.itinerary_animal_record import ItineraryAnimalRecord


@dataclass( frozen=True )
class RestoredTalkCoveredAnimals:
   animals: list[ ItineraryAnimalRecord ]
   replacement_end_seconds: int | None
