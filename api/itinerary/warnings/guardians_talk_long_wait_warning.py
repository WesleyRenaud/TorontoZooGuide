from __future__ import annotations

from ..data_access.validated_itinerary import ValidatedItinerary
from ...models import GuardiansTalk
from ...models import Itinerary
from ...models.guardians_talk_diff import GuardiansTalkDiff
from ..results.itinerary_result_reason import ItineraryResultReason
from ..results.itinerary_save_issue_item import ItinerarySaveIssueItem
from ..scheduling.core.time_block import append_block_from_schedule_times
from ..scheduling.core.time_block import collect_time_blocks_from_itinerary
from ..scheduling.core.time_block import time_block_from_schedule_times
from ..scheduling.core.time_block import time_block_gap_seconds
from ..scheduling.core.time_block import TimeBlock
from ...shared.calendar_dates import DateValues
from ...shared.constants import MAX_GUARDIANS_TALK_WAIT_MINUTES
from ...shared.enums import ItineraryErrorType
from ...shared.enums import ItinerarySaveIssueItemType


def _blocks_without_one_occurrence(
      blocks: list[ TimeBlock ],
      excluded: TimeBlock ) -> list[ TimeBlock ]:
   remaining: list[ TimeBlock ] = []
   removed = False

   for block in blocks:
      if not removed and block == excluded:
         removed = True
         continue

      remaining.append( block )

   return remaining


def _talk_is_isolated(
      talk_block: TimeBlock,
      scheduled_blocks: list[ TimeBlock ] ) -> bool:
   other_blocks = _blocks_without_one_occurrence(
      scheduled_blocks,
      talk_block )

   if not other_blocks:
      return False

   nearest_gap_seconds = min(
      time_block_gap_seconds( talk_block, other_block )
      for other_block in other_blocks )

   return nearest_gap_seconds > MAX_GUARDIANS_TALK_WAIT_MINUTES * 60


def isolated_guardians_talks_from_itinerary(
      itinerary: Itinerary ) -> list[ GuardiansTalk ]:
   scheduled_blocks = collect_time_blocks_from_itinerary( itinerary )

   if len( scheduled_blocks ) < 2:
      return []

   isolated_talks: list[ GuardiansTalk ] = []

   for talk in itinerary.guardians_talks:
      if talk.is_deleted:
         continue

      talk_block = time_block_from_schedule_times(
         talk.start_time,
         talk.end_time )

      if talk_block is None:
         continue

      if _talk_is_isolated( talk_block, scheduled_blocks ):
         isolated_talks.append( talk )

   return isolated_talks


def collect_time_blocks_from_validated_itinerary(
      validated_itinerary: ValidatedItinerary ) -> list[ TimeBlock ]:
   blocks: list[ TimeBlock ] = []

   for animal in validated_itinerary.animals:
      append_block_from_schedule_times(
         blocks,
         animal.start_time,
         animal.end_time )

   for attraction in validated_itinerary.attractions:
      append_block_from_schedule_times(
         blocks,
         attraction.start_time,
         attraction.end_time )

   for event in validated_itinerary.events:
      append_block_from_schedule_times(
         blocks,
         event.start_time,
         event.end_time )

   for talk in validated_itinerary.guardians_talks:
      if talk.is_deleted:
         continue

      append_block_from_schedule_times(
         blocks,
         talk.start_time,
         talk.end_time )

   for encounter in validated_itinerary.wild_encounters:
      if encounter.is_deleted:
         continue

      append_block_from_schedule_times(
         blocks,
         encounter.start_time,
         encounter.end_time )

   return blocks


def isolated_guardians_talks_from_validated_itinerary(
      validated_itinerary: ValidatedItinerary ) -> list[ GuardiansTalkDiff ]:
   scheduled_blocks = collect_time_blocks_from_validated_itinerary(
      validated_itinerary )

   if len( scheduled_blocks ) < 2:
      return []

   isolated_talks: list[ GuardiansTalkDiff ] = []

   for talk in validated_itinerary.guardians_talks:
      if talk.is_deleted:
         continue

      talk_block = time_block_from_schedule_times(
         talk.start_time,
         talk.end_time )

      if talk_block is None:
         continue

      if _talk_is_isolated( talk_block, scheduled_blocks ):
         isolated_talks.append( talk )

   return isolated_talks


def isolated_guardians_talks_after_adding_talk(
      itinerary: Itinerary,
      new_talk: GuardiansTalkDiff ) -> list[ GuardiansTalkDiff ]:
   new_talk_block = time_block_from_schedule_times(
      new_talk.start_time,
      new_talk.end_time )

   if new_talk_block is None:
      return []

   proposed_blocks = [
      *collect_time_blocks_from_itinerary( itinerary ),
      new_talk_block,
   ]

   if len( proposed_blocks ) < 2:
      return []

   if _talk_is_isolated( new_talk_block, proposed_blocks ):
      return [ new_talk ]

   return []


def guardians_talk_long_wait_warning_is_required_for_itinerary(
      itinerary: Itinerary,
      *,
      confirming_guardians_talk_long_wait: bool ) -> bool:
   if confirming_guardians_talk_long_wait:
      return False

   return bool( isolated_guardians_talks_from_itinerary( itinerary ) )


def validated_itinerary_has_unscheduled_listed_items(
      validated_itinerary: ValidatedItinerary ) -> bool:
   for animal in validated_itinerary.animals:
      if not (
            DateValues.normalize_schedule_time_key( animal.start_time )
            and DateValues.normalize_schedule_time_key( animal.end_time ) ):
         return True

   for attraction in validated_itinerary.attractions:
      if not (
            DateValues.normalize_schedule_time_key( attraction.start_time )
            and DateValues.normalize_schedule_time_key( attraction.end_time ) ):
         return True

   return False


def guardians_talk_long_wait_warning_is_required_for_validated_itinerary(
      validated_itinerary: ValidatedItinerary,
      *,
      confirming_guardians_talk_long_wait: bool ) -> bool:
   if confirming_guardians_talk_long_wait:
      return False

   if validated_itinerary_has_unscheduled_listed_items( validated_itinerary ):
      return False

   return bool(
      isolated_guardians_talks_from_validated_itinerary( validated_itinerary ) )


def build_guardians_talk_long_wait_issue_from_talks(
      talks: list[ GuardiansTalk ] | list[ GuardiansTalkDiff ],
      ) -> ItineraryResultReason:
   issue_items = tuple(
      ItinerarySaveIssueItem(
         name=talk.name,
         start_time=talk.start_time,
         end_time=talk.end_time,
         item_type=ItinerarySaveIssueItemType.GUARDIANS_TALK,
         location=getattr( talk, 'location', None ) or '',
      )
      for talk in talks
   )

   return ItineraryResultReason(
      code=ItineraryErrorType.GUARDIANS_TALK_LONG_WAIT,
      items=issue_items )
