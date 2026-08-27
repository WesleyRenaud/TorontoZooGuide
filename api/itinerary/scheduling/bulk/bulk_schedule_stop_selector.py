from __future__ import annotations

from ..core.guest_item_schedule_status import has_itinerary_schedule_times
from ...data_access.itinerary_animal_record import ItineraryAnimalRecord
from ...data_access.itinerary_attraction_record import ItineraryAttractionRecord
from ...data_access.itinerary_transportation_record import ItineraryTransportationRecord
from ...data_access.saved_itinerary import SavedItinerary
from .loop_schedule_stop import LoopScheduleStop


class BulkScheduleStopSelector():
   @classmethod
   def animals(
         cls,
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


   @classmethod
   def attractions(
         cls,
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


   @classmethod
   def transportations(
         cls,
         saved_itinerary: SavedItinerary | None,
         *,
         only_previously_scheduled: bool ) -> list[ ItineraryTransportationRecord ]:
      if saved_itinerary is None:
         return []

      # Transit-mode rows (added_as_attraction=False) are walk-replacement methods,
      # not scenic full-loop packing stops.
      attraction_mode_rows = [
         transportation_row
         for transportation_row in saved_itinerary.transportation_rows
         if transportation_row.added_as_attraction
      ]

      if only_previously_scheduled:
         return [
            transportation_row
            for transportation_row in attraction_mode_rows
            if has_itinerary_schedule_times(
               transportation_row.start_time,
               transportation_row.end_time )
         ]

      return list( attraction_mode_rows )


   @classmethod
   def transit_transportations(
         cls,
         saved_itinerary: SavedItinerary | None ) -> list[ ItineraryTransportationRecord ]:
      if saved_itinerary is None:
         return []

      return [
         transportation_row
         for transportation_row in saved_itinerary.transportation_rows
         if not transportation_row.added_as_attraction
      ]


   @classmethod
   def stops(
         cls,
         saved_itinerary: SavedItinerary | None,
         *,
         only_previously_scheduled: bool ) -> list[ LoopScheduleStop ]:
      return [
         *cls.animals(
            saved_itinerary,
            only_previously_scheduled=only_previously_scheduled ),
         *cls.attractions(
            saved_itinerary,
            only_previously_scheduled=only_previously_scheduled ),
         *cls.transportations(
            saved_itinerary,
            only_previously_scheduled=only_previously_scheduled ),
      ]


   @classmethod
   def stops_matching_previous(
         cls,
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
         if (
               transportation_row.added_as_attraction
               and has_itinerary_schedule_times(
                  transportation_row.start_time,
                  transportation_row.end_time )
         )
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
            if (
                  transportation_row.added_as_attraction
                  and transportation_row.name_key() in previously_scheduled_transportations
            )
         ),
      ]
