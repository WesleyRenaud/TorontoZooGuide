from __future__ import annotations

from ..core.time_block import TimeBlock
from ..core.time_block_builder import TimeBlockBuilder
from ...data_access.itinerary_name_key_builder import ItineraryNameKeyBuilder
from ...data_access.saved_itinerary import SavedItinerary
from ...data_access.validated_itinerary import ValidatedItinerary
from .fixed_time_activity_unschedule_preparer import FixedTimeActivityUnschedulePreparer
from ....models.guardians_talk_diff import GuardiansTalkDiff
from ....types import Cursor


class GuardiansTalkUnschedulePreparer():
   @classmethod
   def time_blocks(
         cls,
         guardians_talks: list[ GuardiansTalkDiff ] ) -> list[ TimeBlock ]:
      return [
         TimeBlockBuilder.from_schedule_times(
            guardians_talk.start_time,
            guardians_talk.end_time )
         for guardians_talk in guardians_talks
      ]


   @classmethod
   def newly_added_active(
         cls,
         saved_itinerary: SavedItinerary,
         guardians_talks: list[ GuardiansTalkDiff ] ) -> list[ GuardiansTalkDiff ]:
      saved_names = {
         ItineraryNameKeyBuilder.build( row.talk_name )
         for row in saved_itinerary.guardians_talk_rows
         if not row.is_deleted
      }

      return [
         guardians_talk
         for guardians_talk in guardians_talks
         if (
            ItineraryNameKeyBuilder.build( guardians_talk.name ) not in saved_names
            and not guardians_talk.is_deleted
            and TimeBlockBuilder.from_schedule_times(
               guardians_talk.start_time,
               guardians_talk.end_time ) is not None
         )
      ]


   @classmethod
   def saved_itinerary_has_overlap(
         cls,
         saved_itinerary: SavedItinerary,
         new_guardians_talks: list[ GuardiansTalkDiff ] ) -> bool:
      return FixedTimeActivityUnschedulePreparer.saved_itinerary_has_overlap(
         saved_itinerary,
         cls.time_blocks( new_guardians_talks ) )


   @classmethod
   def prepare_validated_for_reschedule(
         cls,
         validated_itinerary: ValidatedItinerary,
         new_guardians_talks: list[ GuardiansTalkDiff ] ) -> ValidatedItinerary:
      return FixedTimeActivityUnschedulePreparer.prepare_validated_for_reschedule(
         validated_itinerary,
         cls.time_blocks( new_guardians_talks ) )


   @classmethod
   def apply_to_validated_itinerary(
         cls,
         validated_itinerary: ValidatedItinerary,
         new_guardians_talks: list[ GuardiansTalkDiff ] ) -> ValidatedItinerary:
      return cls.prepare_validated_for_reschedule(
         validated_itinerary,
         new_guardians_talks )


   @classmethod
   def clear_overlapping_saved_schedules(
         cls,
         cur: Cursor,
         saved_itinerary: SavedItinerary,
         new_guardians_talks: list[ GuardiansTalkDiff ] ) -> None:
      FixedTimeActivityUnschedulePreparer.clear_overlapping_saved_schedules(
         cur,
         saved_itinerary,
         cls.time_blocks( new_guardians_talks ) )
