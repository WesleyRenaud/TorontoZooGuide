from __future__ import annotations

from ..core.time_block import TimeBlock
from ..core.time_block_builder import TimeBlockBuilder
from ...data_access.itinerary_name_key_builder import ItineraryNameKeyBuilder
from ...data_access.saved_itinerary import SavedItinerary
from ...data_access.validated_itinerary import ValidatedItinerary
from .fixed_time_activity_unschedule_items import clear_saved_schedules_overlapping_time_blocks
from .fixed_time_activity_unschedule_items import prepare_validated_itinerary_for_fixed_time_activity_reschedule
from .fixed_time_activity_unschedule_items import saved_itinerary_has_overlap_with_time_blocks
from ....models.guardians_talk_diff import GuardiansTalkDiff
from ....types import Cursor


def guardians_talk_time_blocks(
      guardians_talks: list[ GuardiansTalkDiff ] ) -> list[ TimeBlock ]:
   return [
      TimeBlockBuilder.from_schedule_times(
         guardians_talk.start_time,
         guardians_talk.end_time )
      for guardians_talk in guardians_talks
   ]


def newly_added_active_guardians_talks(
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


def saved_itinerary_has_overlap_with_guardians_talks(
      saved_itinerary: SavedItinerary,
      new_guardians_talks: list[ GuardiansTalkDiff ] ) -> bool:
   return saved_itinerary_has_overlap_with_time_blocks(
      saved_itinerary,
      guardians_talk_time_blocks( new_guardians_talks ) )


def prepare_validated_itinerary_for_guardians_talk_reschedule(
      validated_itinerary: ValidatedItinerary,
      new_guardians_talks: list[ GuardiansTalkDiff ] ) -> ValidatedItinerary:
   return prepare_validated_itinerary_for_fixed_time_activity_reschedule(
      validated_itinerary,
      guardians_talk_time_blocks( new_guardians_talks ) )


def apply_guardians_talk_unschedule_to_validated_itinerary(
      validated_itinerary: ValidatedItinerary,
      new_guardians_talks: list[ GuardiansTalkDiff ] ) -> ValidatedItinerary:
   return prepare_validated_itinerary_for_guardians_talk_reschedule(
      validated_itinerary,
      new_guardians_talks )


def clear_saved_schedules_overlapping_guardians_talks(
      cur: Cursor,
      saved_itinerary: SavedItinerary,
      new_guardians_talks: list[ GuardiansTalkDiff ] ) -> None:
   clear_saved_schedules_overlapping_time_blocks(
      cur,
      saved_itinerary,
      guardians_talk_time_blocks( new_guardians_talks ) )
