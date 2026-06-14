from __future__ import annotations

from ...models.guardians_talk_diff import GuardiansTalkDiff
from ...models.wild_encounter_diff import WildEncounterDiff
from ..results.itinerary_result_reason import ItineraryResultReason
from ..results.itinerary_save_issue_item import ItinerarySaveIssueItem
from ..scheduling.core.time_block import time_block_from_schedule_times
from ...shared.calendar_dates import DateValues
from ...shared.enums import ItineraryErrorType
from ...types import ScheduledItem


def schedule_time_range( scheduled_item: ScheduledItem ) -> tuple[ int, int ] | None:
   time_block = time_block_from_schedule_times(
      scheduled_item.start_time,
      scheduled_item.end_time )

   if time_block is None:
      return None

   return ( time_block.start_seconds, time_block.end_seconds )


def schedule_times_overlap(
      first: ScheduledItem,
      second: ScheduledItem ) -> bool:
   first_start, first_end = schedule_time_range( first )
   second_start, second_end = schedule_time_range( second )

   return first_start < second_end and second_start < first_end


def active_scheduled_items(
      guardians_talks: list[ GuardiansTalkDiff ],
      wild_encounters: list[ WildEncounterDiff ] ) -> list[ ScheduledItem ]:
   active_talks = [
      guardians_talk
      for guardians_talk in guardians_talks
      if (
         not guardians_talk.is_deleted
         and schedule_time_range( guardians_talk ) is not None
      )
   ]
   active_encounters = [
      wild_encounter
      for wild_encounter in wild_encounters
      if (
         not wild_encounter.is_deleted
         and schedule_time_range( wild_encounter ) is not None
      )
   ]

   return active_talks + active_encounters


def collect_overlapping_group(
      scheduled_items: list[ ScheduledItem ],
      start_index: int,
      visited: set[ int ] ) -> list[ ScheduledItem ]:
   group: list[ ScheduledItem ] = []
   pending_indices = [ start_index ]
   visited.add( start_index )

   while pending_indices:
      current_index = pending_indices.pop()
      current_item = scheduled_items[ current_index ]
      group.append( current_item )

      for other_index, other_item in enumerate( scheduled_items ):
         if other_index in visited:
            continue

         if not schedule_times_overlap( current_item, other_item ):
            continue

         visited.add( other_index )
         pending_indices.append( other_index )

   return group


def find_schedule_time_conflict_groups(
      scheduled_items: list[ ScheduledItem ] ) -> list[ list[ ScheduledItem ] ]:
   if len( scheduled_items ) < 2:
      return []

   visited: set[ int ] = set()
   conflict_groups: list[ list[ ScheduledItem ] ] = []

   for start_index in range( len( scheduled_items ) ):
      if start_index in visited:
         continue

      group = collect_overlapping_group(
         scheduled_items,
         start_index,
         visited )

      if len( group ) > 1:
         conflict_groups.append( group )

   return conflict_groups


def scheduled_item_to_issue_item(
      scheduled_item: ScheduledItem ) -> ItinerarySaveIssueItem:
   if isinstance( scheduled_item, GuardiansTalkDiff ):
      return ItinerarySaveIssueItem.from_guardians_talk_diff( scheduled_item )

   return ItinerarySaveIssueItem.from_wild_encounter_diff( scheduled_item )


def sort_scheduled_items_for_issue(
      scheduled_items: list[ ScheduledItem ] ) -> list[ ScheduledItem ]:
   return sorted(
      scheduled_items,
      key=lambda scheduled_item: (
         DateValues.time_value_in_minutes( scheduled_item.start_time )
         or 0,
         scheduled_item.name,
      ) )


def build_schedule_time_conflict_issue(
      scheduled_items: list[ ScheduledItem ] ) -> ItineraryResultReason:
   sorted_items = sort_scheduled_items_for_issue( scheduled_items )
   issue_items = tuple(
      scheduled_item_to_issue_item( scheduled_item )
      for scheduled_item in sorted_items
   )

   return ItineraryResultReason(
      code=ItineraryErrorType.WILD_ENCOUNTER_TIME_CONFLICT,
      items=issue_items )


def find_schedule_time_conflict_issues(
      guardians_talks: list[ GuardiansTalkDiff ],
      wild_encounters: list[ WildEncounterDiff ] ) -> tuple[ ItineraryResultReason, ... ]:
   scheduled_items = active_scheduled_items( guardians_talks, wild_encounters )
   conflict_groups = find_schedule_time_conflict_groups( scheduled_items )

   if not conflict_groups:
      return ()

   return tuple(
      build_schedule_time_conflict_issue( group )
      for group in conflict_groups
   )
