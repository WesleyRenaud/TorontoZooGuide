from __future__ import annotations

from ..core.time_block import time_block_from_schedule_times
from ..core.time_block import TimeBlock
from ...data_access.itinerary_name_key import itinerary_name_key
from ...data_access.saved_itinerary import SavedItinerary
from ...data_access.validated_itinerary import ValidatedItinerary
from .fixed_time_activity_unschedule_items import clear_saved_schedules_overlapping_time_blocks
from .fixed_time_activity_unschedule_items import prepare_validated_itinerary_for_fixed_time_activity_reschedule
from .fixed_time_activity_unschedule_items import saved_itinerary_has_overlap_with_time_blocks
from ....models.wild_encounter_diff import WildEncounterDiff
from ....types import Cursor


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


def saved_itinerary_has_overlap_with_wild_encounters(
      saved_itinerary: SavedItinerary,
      new_wild_encounters: list[ WildEncounterDiff ] ) -> bool:
   return saved_itinerary_has_overlap_with_time_blocks(
      saved_itinerary,
      wild_encounter_time_blocks( new_wild_encounters ) )


def prepare_validated_itinerary_for_wild_encounter_reschedule(
      validated_itinerary: ValidatedItinerary,
      new_wild_encounters: list[ WildEncounterDiff ] ) -> ValidatedItinerary:
   return prepare_validated_itinerary_for_fixed_time_activity_reschedule(
      validated_itinerary,
      wild_encounter_time_blocks( new_wild_encounters ) )


def apply_wild_encounter_unschedule_to_validated_itinerary(
      validated_itinerary: ValidatedItinerary,
      new_wild_encounters: list[ WildEncounterDiff ] ) -> ValidatedItinerary:
   return prepare_validated_itinerary_for_wild_encounter_reschedule(
      validated_itinerary,
      new_wild_encounters )


def clear_saved_schedules_overlapping_wild_encounters(
      cur: Cursor,
      saved_itinerary: SavedItinerary,
      new_wild_encounters: list[ WildEncounterDiff ] ) -> None:
   clear_saved_schedules_overlapping_time_blocks(
      cur,
      saved_itinerary,
      wild_encounter_time_blocks( new_wild_encounters ) )
