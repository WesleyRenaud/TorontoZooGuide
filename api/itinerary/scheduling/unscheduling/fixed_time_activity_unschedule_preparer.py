from __future__ import annotations

from ..core.time_block import TimeBlock
from ..core.time_block_builder import TimeBlockBuilder
from ...data_access.saved_itinerary import SavedItinerary
from ...data_access.unschedule_itinerary_item_provider import UnscheduleItineraryItemProvider
from ...data_access.validated_itinerary import ValidatedItinerary
from ....types import Types


class FixedTimeActivityUnschedulePreparer():
   @classmethod
   def overlaps_any_time_block(
         cls,
         start_time: Types.ScheduleTimeKey,
         end_time: Types.ScheduleTimeKey,
         activity_blocks: list[ TimeBlock ] ) -> bool:
      item_block = TimeBlockBuilder.from_schedule_times( start_time, end_time )

      if item_block is None:
         return False

      return any(
         TimeBlockBuilder.overlap( item_block, activity_block )
         for activity_block in activity_blocks
      )


   @classmethod
   def saved_itinerary_has_overlap(
         cls,
         saved_itinerary: SavedItinerary,
         activity_blocks: list[ TimeBlock ] ) -> bool:
      for animal in saved_itinerary.animal_rows:
         if cls.overlaps_any_time_block(
               animal.start_time,
               animal.end_time,
               activity_blocks ):
            return True

      for attraction in saved_itinerary.attraction_rows:
         if cls.overlaps_any_time_block(
               attraction.start_time,
               attraction.end_time,
               activity_blocks ):
            return True

      for transportation in saved_itinerary.transportation_rows:
         if cls.overlaps_any_time_block(
               transportation.start_time,
               transportation.end_time,
               activity_blocks ):
            return True

      for event in saved_itinerary.event_rows:
         if cls.overlaps_any_time_block(
               event.start_time,
               event.end_time,
               activity_blocks ):
            return True

      return False


   @classmethod
   def remove_overlapping_events(
         cls,
         validated_itinerary: ValidatedItinerary,
         activity_blocks: list[ TimeBlock ] ) -> None:
      validated_itinerary.events[ : ] = [
         event
         for event in validated_itinerary.events
         if not cls.overlaps_any_time_block(
               event.start_time,
               event.end_time,
               activity_blocks )
      ]


   @classmethod
   def prepare_validated_for_reschedule(
         cls,
         validated_itinerary: ValidatedItinerary,
         activity_blocks: list[ TimeBlock ] ) -> ValidatedItinerary:
      cls.remove_overlapping_events(
         validated_itinerary,
         activity_blocks )

      for animal in validated_itinerary.animals:
         animal.start_time = None
         animal.end_time = None

      for attraction in validated_itinerary.attractions:
         attraction.start_time = None
         attraction.end_time = None

      for transportation in validated_itinerary.transportations:
         transportation.start_time = None
         transportation.end_time = None
         transportation.legs = []

      return validated_itinerary


   @classmethod
   def clear_overlapping_saved_schedules(
         cls,
         cur: Types.Cursor,
         saved_itinerary: SavedItinerary,
         activity_blocks: list[ TimeBlock ] ) -> None:
      for animal in saved_itinerary.animal_rows:
         if cls.overlaps_any_time_block(
               animal.start_time,
               animal.end_time,
               activity_blocks ):
            UnscheduleItineraryItemProvider.clear_itinerary_animal_schedule(
               cur,
               species=animal.species,
               exhibit=animal.exhibit )

      for attraction in saved_itinerary.attraction_rows:
         if cls.overlaps_any_time_block(
               attraction.start_time,
               attraction.end_time,
               activity_blocks ):
            UnscheduleItineraryItemProvider.clear_itinerary_attraction_schedule(
               cur,
               name=attraction.attraction )

      for transportation in saved_itinerary.transportation_rows:
         if cls.overlaps_any_time_block(
               transportation.start_time,
               transportation.end_time,
               activity_blocks ):
            UnscheduleItineraryItemProvider.clear_itinerary_transportation_schedule(
               cur,
               name=transportation.transportation,
               added_as_attraction=transportation.added_as_attraction )

      for event in saved_itinerary.event_rows:
         if cls.overlaps_any_time_block(
               event.start_time,
               event.end_time,
               activity_blocks ):
            UnscheduleItineraryItemProvider.delete_itinerary_event_schedule(
               cur,
               event_type=event.event_type )
