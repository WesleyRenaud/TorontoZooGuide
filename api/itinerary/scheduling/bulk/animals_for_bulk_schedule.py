from __future__ import annotations

from .bulk_schedule_animals import has_itinerary_schedule_times
from ...data_access.itinerary_animal_record import ItineraryAnimalRecord
from ...data_access.itinerary_attraction_record import ItineraryAttractionRecord
from ...data_access.itinerary_transportation_record import ItineraryTransportationRecord
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


def transportations_for_bulk_schedule(
      saved_itinerary: SavedItinerary | None,
      *,
      only_previously_scheduled: bool ) -> list[ ItineraryTransportationRecord ]:
   if saved_itinerary is None:
      return []

   if only_previously_scheduled:
      return [
         transportation_row
         for transportation_row in saved_itinerary.transportation_rows
         if has_itinerary_schedule_times(
            transportation_row.start_time,
            transportation_row.end_time )
      ]

   return list( saved_itinerary.transportation_rows )


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
      *transportations_for_bulk_schedule(
         saved_itinerary,
         only_previously_scheduled=only_previously_scheduled ),
   ]


def stops_for_bulk_schedule_matching_previous(
      saved_itinerary_before_clear: SavedItinerary | None,
      saved_itinerary_after_save: SavedItinerary ) -> list[ LoopScheduleStop ]:
   # previously scheduled species may have a new enclosure after validate
   # (outdoor Aldabra → indoor). Pack the post-save row, not the removed spot —
   # persisting the old enclosure fails and aborts the rest of the loop group.
   if saved_itinerary_before_clear is None:
      return []

   previously_scheduled_species_exhibits = {
      animal_row.species_exhibit_key()
      for animal_row in saved_itinerary_before_clear.animal_rows
      if has_itinerary_schedule_times(
         animal_row.start_time,
         animal_row.end_time )
   }
   previously_scheduled_attractions = {
      attraction_row.name_key()
      for attraction_row in saved_itinerary_before_clear.attraction_rows
      if has_itinerary_schedule_times(
         attraction_row.start_time,
         attraction_row.end_time )
   }
   previously_scheduled_transportations = {
      transportation_row.name_key()
      for transportation_row in saved_itinerary_before_clear.transportation_rows
      if has_itinerary_schedule_times(
         transportation_row.start_time,
         transportation_row.end_time )
   }

   return [
      *(
         animal_row
         for animal_row in saved_itinerary_after_save.animal_rows
         if animal_row.species_exhibit_key() in previously_scheduled_species_exhibits
      ),
      *(
         attraction_row
         for attraction_row in saved_itinerary_after_save.attraction_rows
         if attraction_row.name_key() in previously_scheduled_attractions
      ),
      *(
         transportation_row
         for transportation_row in saved_itinerary_after_save.transportation_rows
         if transportation_row.name_key() in previously_scheduled_transportations
      ),
   ]
