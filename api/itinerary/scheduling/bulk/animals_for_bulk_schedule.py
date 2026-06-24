from __future__ import annotations

from .bulk_schedule_animals import has_itinerary_schedule_times
from ...data_access.itinerary_animal_record import ItineraryAnimalRecord
from ...data_access.saved_itinerary import SavedItinerary


def animals_for_bulk_schedule(
      saved_itinerary: SavedItinerary | None,
      *,
      only_previously_scheduled: bool ) -> list[ ItineraryAnimalRecord ]:
   if saved_itinerary is None:
      return []

   if only_previously_scheduled:
      return [
         animal_row
         for animal_row in saved_itinerary.animal_rows
         if has_itinerary_schedule_times(
            animal_row.start_time,
            animal_row.end_time )
      ]

   return list( saved_itinerary.animal_rows )
