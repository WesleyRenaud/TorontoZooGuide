from __future__ import annotations

from ..core.time_block import TimeBlock
from ..core.time_block_builder import TimeBlockBuilder
from ...data_access.itinerary_name_key_builder import ItineraryNameKeyBuilder
from ...data_access.saved_itinerary import SavedItinerary
from ...data_access.validated_itinerary import ValidatedItinerary
from .fixed_time_activity_unschedule_preparer import FixedTimeActivityUnschedulePreparer
from ....models.wild_encounter_diff import WildEncounterDiff
from ....types import Types


class WildEncounterUnschedulePreparer():
   @classmethod
   def time_blocks(
         cls,
         wild_encounters: list[ WildEncounterDiff ] ) -> list[ TimeBlock ]:
      return [
         TimeBlockBuilder.from_schedule_times(
            wild_encounter.start_time,
            wild_encounter.end_time )
         for wild_encounter in wild_encounters
      ]


   @classmethod
   def newly_added_active(
         cls,
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
            ItineraryNameKeyBuilder.build( wild_encounter.name ) not in saved_names
            and not wild_encounter.is_deleted
            and TimeBlockBuilder.from_schedule_times(
               wild_encounter.start_time,
               wild_encounter.end_time ) is not None
         )
      ]


   @classmethod
   def saved_itinerary_has_overlap(
         cls,
         saved_itinerary: SavedItinerary,
         new_wild_encounters: list[ WildEncounterDiff ] ) -> bool:
      return FixedTimeActivityUnschedulePreparer.saved_itinerary_has_overlap(
         saved_itinerary,
         cls.time_blocks( new_wild_encounters ) )


   @classmethod
   def prepare_validated_for_reschedule(
         cls,
         validated_itinerary: ValidatedItinerary,
         new_wild_encounters: list[ WildEncounterDiff ] ) -> ValidatedItinerary:
      return FixedTimeActivityUnschedulePreparer.prepare_validated_for_reschedule(
         validated_itinerary,
         cls.time_blocks( new_wild_encounters ) )


   @classmethod
   def apply_to_validated_itinerary(
         cls,
         validated_itinerary: ValidatedItinerary,
         new_wild_encounters: list[ WildEncounterDiff ] ) -> ValidatedItinerary:
      return cls.prepare_validated_for_reschedule(
         validated_itinerary,
         new_wild_encounters )


   @classmethod
   def clear_overlapping_saved_schedules(
         cls,
         cur: Types.Cursor,
         saved_itinerary: SavedItinerary,
         new_wild_encounters: list[ WildEncounterDiff ] ) -> None:
      FixedTimeActivityUnschedulePreparer.clear_overlapping_saved_schedules(
         cur,
         saved_itinerary,
         cls.time_blocks( new_wild_encounters ) )
