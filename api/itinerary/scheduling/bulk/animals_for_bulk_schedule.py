from __future__ import annotations

from .bulk_schedule_animals import has_itinerary_schedule_times
from ...data_access.itinerary_animal_record import ItineraryAnimalRecord
from ...data_access.itinerary_attraction_record import ItineraryAttractionRecord
from ...data_access.saved_itinerary import SavedItinerary
from .loop_schedule_stop import LoopScheduleStop


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


def attractions_for_bulk_schedule(
      saved_itinerary: SavedItinerary | None,
      *,
      only_previously_scheduled: bool ) -> list[ ItineraryAttractionRecord ]:
   if saved_itinerary is None:
      return []

   if only_previously_scheduled:
      return [
         attraction_row
         for attraction_row in saved_itinerary.attraction_rows
         if has_itinerary_schedule_times(
            attraction_row.start_time,
            attraction_row.end_time )
      ]

   return list( saved_itinerary.attraction_rows )


def stops_for_bulk_schedule(
      saved_itinerary: SavedItinerary | None,
      *,
      only_previously_scheduled: bool ) -> list[ LoopScheduleStop ]:
   return [
      *animals_for_bulk_schedule(
         saved_itinerary,
         only_previously_scheduled=only_previously_scheduled ),
      *attractions_for_bulk_schedule(
         saved_itinerary,
         only_previously_scheduled=only_previously_scheduled ),
   ]
