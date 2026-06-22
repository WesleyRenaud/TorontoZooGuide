from __future__ import annotations

from ..core.time_block import time_block_from_schedule_times
from ..core.time_block import time_blocks_overlap
from ..core.time_block import TimeBlock
from ...data_access.saved_itinerary import SavedItinerary
from ...data_access.unschedule_itinerary_item import clear_itinerary_animal_schedule
from ...data_access.unschedule_itinerary_item import clear_itinerary_attraction_schedule
from ...data_access.unschedule_itinerary_item import delete_itinerary_event_schedule
from ...data_access.validated_itinerary import ValidatedItinerary
from ....types import Cursor
from ....types import ScheduleTimeKey


def schedule_overlaps_any_time_block(
      start_time: ScheduleTimeKey,
      end_time: ScheduleTimeKey,
      activity_blocks: list[ TimeBlock ] ) -> bool:
   item_block = time_block_from_schedule_times( start_time, end_time )

   if item_block is None:
      return False

   return any(
      time_blocks_overlap( item_block, activity_block )
      for activity_block in activity_blocks
   )


def saved_itinerary_has_overlap_with_time_blocks(
      saved_itinerary: SavedItinerary,
      activity_blocks: list[ TimeBlock ] ) -> bool:
   for animal in saved_itinerary.animal_rows:
      if schedule_overlaps_any_time_block(
            animal.start_time,
            animal.end_time,
            activity_blocks ):
         return True

   for attraction in saved_itinerary.attraction_rows:
      if schedule_overlaps_any_time_block(
            attraction.start_time,
            attraction.end_time,
            activity_blocks ):
         return True

   for event in saved_itinerary.event_rows:
      if schedule_overlaps_any_time_block(
            event.start_time,
            event.end_time,
            activity_blocks ):
         return True

   return False


def remove_events_overlapping_time_blocks(
      validated_itinerary: ValidatedItinerary,
      activity_blocks: list[ TimeBlock ] ) -> None:
   validated_itinerary.events[ : ] = [
      event
      for event in validated_itinerary.events
      if not schedule_overlaps_any_time_block(
            event.start_time,
            event.end_time,
            activity_blocks )
   ]


def prepare_validated_itinerary_for_fixed_time_activity_reschedule(
      validated_itinerary: ValidatedItinerary,
      activity_blocks: list[ TimeBlock ] ) -> ValidatedItinerary:
   remove_events_overlapping_time_blocks(
      validated_itinerary,
      activity_blocks )

   for animal in validated_itinerary.animals:
      animal.start_time = None
      animal.end_time = None

   for attraction in validated_itinerary.attractions:
      attraction.start_time = None
      attraction.end_time = None

   return validated_itinerary


def clear_saved_schedules_overlapping_time_blocks(
      cur: Cursor,
      saved_itinerary: SavedItinerary,
      activity_blocks: list[ TimeBlock ] ) -> None:
   for animal in saved_itinerary.animal_rows:
      if schedule_overlaps_any_time_block(
            animal.start_time,
            animal.end_time,
            activity_blocks ):
         clear_itinerary_animal_schedule(
            cur,
            species=animal.species,
            exhibit=animal.exhibit )

   for attraction in saved_itinerary.attraction_rows:
      if schedule_overlaps_any_time_block(
            attraction.start_time,
            attraction.end_time,
            activity_blocks ):
         clear_itinerary_attraction_schedule(
            cur,
            name=attraction.attraction )

   for event in saved_itinerary.event_rows:
      if schedule_overlaps_any_time_block(
            event.start_time,
            event.end_time,
            activity_blocks ):
         delete_itinerary_event_schedule(
            cur,
            event_type=event.event_type )
