from __future__ import annotations

from ..core.time_block import time_block_from_schedule_times
from ..core.time_block import time_blocks_overlap
from ..core.time_block import TimeBlock
from ...data_access.itinerary_name_key import itinerary_name_key
from ...data_access.saved_itinerary import SavedItinerary
from ...data_access.unschedule_itinerary_item import clear_itinerary_animal_schedule
from ...data_access.unschedule_itinerary_item import clear_itinerary_attraction_schedule
from ...data_access.unschedule_itinerary_item import delete_itinerary_event_schedule
from ...data_access.validated_itinerary import ValidatedItinerary
from ....models.guardians_talk_diff import GuardiansTalkDiff
from ....types import Cursor
from ....types import ScheduleTimeKey


def guardians_talk_time_blocks(
      guardians_talks: list[ GuardiansTalkDiff ] ) -> list[ TimeBlock ]:
   return [
      time_block_from_schedule_times(
         guardians_talk.start_time,
         guardians_talk.end_time )
      for guardians_talk in guardians_talks
   ]


def newly_added_active_guardians_talks(
      saved_itinerary: SavedItinerary,
      guardians_talks: list[ GuardiansTalkDiff ] ) -> list[ GuardiansTalkDiff ]:
   saved_names = {
      itinerary_name_key( row.talk_name )
      for row in saved_itinerary.guardians_talk_rows
      if not row.is_deleted
   }

   return [
      guardians_talk
      for guardians_talk in guardians_talks
      if (
         itinerary_name_key( guardians_talk.name ) not in saved_names
         and time_block_from_schedule_times(
            guardians_talk.start_time,
            guardians_talk.end_time ) is not None
      )
   ]


def _schedule_overlaps_any_block(
      start_time: ScheduleTimeKey,
      end_time: ScheduleTimeKey,
      talk_blocks: list[ TimeBlock ] ) -> bool:
   item_block = time_block_from_schedule_times( start_time, end_time )

   if item_block is None:
      return False

   return any(
      time_blocks_overlap( item_block, talk_block )
      for talk_block in talk_blocks
   )


def saved_itinerary_has_overlap_with_guardians_talks(
      saved_itinerary: SavedItinerary,
      new_guardians_talks: list[ GuardiansTalkDiff ] ) -> bool:
   talk_blocks = guardians_talk_time_blocks( new_guardians_talks )

   for animal in saved_itinerary.animal_rows:
      if _schedule_overlaps_any_block(
            animal.start_time,
            animal.end_time,
            talk_blocks ):
         return True

   for attraction in saved_itinerary.attraction_rows:
      if _schedule_overlaps_any_block(
            attraction.start_time,
            attraction.end_time,
            talk_blocks ):
         return True

   for event in saved_itinerary.event_rows:
      if _schedule_overlaps_any_block(
            event.start_time,
            event.end_time,
            talk_blocks ):
         return True

   return False


def apply_guardians_talk_unschedule_to_validated_itinerary(
      validated_itinerary: ValidatedItinerary,
      new_guardians_talks: list[ GuardiansTalkDiff ] ) -> ValidatedItinerary:
   talk_blocks = guardians_talk_time_blocks( new_guardians_talks )

   for animal in validated_itinerary.animals:
      if _schedule_overlaps_any_block(
            animal.start_time,
            animal.end_time,
            talk_blocks ):
         animal.start_time = None
         animal.end_time = None

   for attraction in validated_itinerary.attractions:
      if _schedule_overlaps_any_block(
            attraction.start_time,
            attraction.end_time,
            talk_blocks ):
         attraction.start_time = None
         attraction.end_time = None

   validated_itinerary.events[ : ] = [
      event
      for event in validated_itinerary.events
      if not _schedule_overlaps_any_block(
            event.start_time,
            event.end_time,
            talk_blocks )
   ]

   return validated_itinerary


def clear_saved_schedules_overlapping_guardians_talks(
      cur: Cursor,
      saved_itinerary: SavedItinerary,
      new_guardians_talks: list[ GuardiansTalkDiff ] ) -> None:
   talk_blocks = guardians_talk_time_blocks( new_guardians_talks )

   for animal in saved_itinerary.animal_rows:
      if _schedule_overlaps_any_block(
            animal.start_time,
            animal.end_time,
            talk_blocks ):
         clear_itinerary_animal_schedule(
            cur,
            species=animal.species,
            exhibit=animal.exhibit )

   for attraction in saved_itinerary.attraction_rows:
      if _schedule_overlaps_any_block(
            attraction.start_time,
            attraction.end_time,
            talk_blocks ):
         clear_itinerary_attraction_schedule(
            cur,
            name=attraction.attraction )

   for event in saved_itinerary.event_rows:
      if _schedule_overlaps_any_block(
            event.start_time,
            event.end_time,
            talk_blocks ):
         delete_itinerary_event_schedule(
            cur,
            event_type=event.event_type )
