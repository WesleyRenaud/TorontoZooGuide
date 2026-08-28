from __future__ import annotations

from typing import TypeAlias

from ...data_access.itinerary_animal_record import ItineraryAnimalRecord
from ...data_access.itinerary_attraction_record import ItineraryAttractionRecord
from ...data_access.itinerary_transportation_record import ItineraryTransportationRecord


class LoopScheduleStop():
   Stop: TypeAlias = (
      ItineraryAnimalRecord
      | ItineraryAttractionRecord
      | ItineraryTransportationRecord
   )
