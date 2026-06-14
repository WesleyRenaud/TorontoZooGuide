from __future__ import annotations

from ..data_access.itinerary_name_key import itinerary_name_key
from ..data_access.saved_itinerary import SavedItinerary
from ..data_access.unschedule_itinerary_item import clear_itinerary_animal_schedule
from ..data_access.unschedule_itinerary_item import clear_itinerary_attraction_schedule
from ..data_access.unschedule_itinerary_item import delete_itinerary_event_schedule
from ..data_access.validated_itinerary import ValidatedItinerary
from ...models.wild_encounter_diff import WildEncounterDiff
from ..scheduling.core.time_block import time_block_from_schedule_times
from ..scheduling.core.time_block import time_blocks_overlap
from ..scheduling.core.time_block import TimeBlock
from ...types import Cursor
from ...types import ScheduleTimeKey


def wild_encounter_time_blocks(
      wild_encounters: list[ WildEncounterDiff ] ) -> list[ TimeBlock ]:
   return [
      time_block_from_schedule_times(
         wild_encounter.start_time,
         wild_encounter.end_time )
      for wild_encounter in wild_encounters
   ]


def newly_added_active_wild_encounters(
      saved_itinerary: SavedItinerary,
      wild_encounters: list[ WildEncounterDiff ] ) -> list[ WildEncounterDiff ]:
   saved_names = {
      row.name_key()
      for row in saved_itinerary.wild_encounter_rows
      if not row.is_deleted
   }

   return [
      wild_encounter
      for wild_encounter in wild_encounters
      if (
         itinerary_name_key( wild_encounter.name ) not in saved_names
         and not wild_encounter.is_deleted
         and time_block_from_schedule_times(
            wild_encounter.start_time,
            wild_encounter.end_time ) is not None
      )
   ]


def _schedule_overlaps_any_block(
      start_time: ScheduleTimeKey,
      end_time: ScheduleTimeKey,
      encounter_blocks: list[ TimeBlock ] ) -> bool:
   item_block = time_block_from_schedule_times( start_time, end_time )

   if item_block is None:
      return False

   return any(
      time_blocks_overlap( item_block, encounter_block )
      for encounter_block in encounter_blocks
   )


def saved_itinerary_has_overlap_with_wild_encounters(
      saved_itinerary: SavedItinerary,
      new_wild_encounters: list[ WildEncounterDiff ] ) -> bool:
   encounter_blocks = wild_encounter_time_blocks( new_wild_encounters )

   for animal in saved_itinerary.animal_rows:
      if _schedule_overlaps_any_block(
            animal.start_time,
            animal.end_time,
            encounter_blocks ):
         return True

   for attraction in saved_itinerary.attraction_rows:
      if _schedule_overlaps_any_block(
            attraction.start_time,
            attraction.end_time,
            encounter_blocks ):
         return True

   for event in saved_itinerary.event_rows:
      if _schedule_overlaps_any_block(
            event.start_time,
            event.end_time,
            encounter_blocks ):
         return True

   return False


def apply_wild_encounter_unschedule_to_validated_itinerary(
      validated_itinerary: ValidatedItinerary,
      new_wild_encounters: list[ WildEncounterDiff ] ) -> ValidatedItinerary:
   encounter_blocks = wild_encounter_time_blocks( new_wild_encounters )

   for animal in validated_itinerary.animals:
      if _schedule_overlaps_any_block(
            animal.start_time,
            animal.end_time,
            encounter_blocks ):
         animal.start_time = None
         animal.end_time = None

   for attraction in validated_itinerary.attractions:
      if _schedule_overlaps_any_block(
            attraction.start_time,
            attraction.end_time,
            encounter_blocks ):
         attraction.start_time = None
         attraction.end_time = None

   validated_itinerary.events[ : ] = [
      event
      for event in validated_itinerary.events
      if not _schedule_overlaps_any_block(
            event.start_time,
            event.end_time,
            encounter_blocks )
   ]

   return validated_itinerary


def clear_saved_schedules_overlapping_wild_encounters(
      cur: Cursor,
      saved_itinerary: SavedItinerary,
      new_wild_encounters: list[ WildEncounterDiff ] ) -> None:
   encounter_blocks = wild_encounter_time_blocks( new_wild_encounters )

   for animal in saved_itinerary.animal_rows:
      if _schedule_overlaps_any_block(
            animal.start_time,
            animal.end_time,
            encounter_blocks ):
         clear_itinerary_animal_schedule(
            cur,
            species=animal.species,
            exhibit=animal.exhibit )

   for attraction in saved_itinerary.attraction_rows:
      if _schedule_overlaps_any_block(
            attraction.start_time,
            attraction.end_time,
            encounter_blocks ):
         clear_itinerary_attraction_schedule(
            cur,
            name=attraction.attraction )

   for event in saved_itinerary.event_rows:
      if _schedule_overlaps_any_block(
            event.start_time,
            event.end_time,
            encounter_blocks ):
         delete_itinerary_event_schedule(
            cur,
            event_type=event.event_type )
