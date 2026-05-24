from __future__ import annotations

from .itinerary_save_issue import ItinerarySaveIssue
from .itinerary_save_issue_item import ItinerarySaveIssueItem
from ...models.guardians_talk_diff import GuardiansTalkDiff
from ...models.wild_encounter_diff import WildEncounterDiff
from ...shared.date_values import DateValues
from ...shared.enums import ItinerarySaveIssueType
from ...types import ScheduledItem


def schedule_time_range( scheduled_item: ScheduledItem ) -> tuple[ int, int ]:
   start_time = DateValues.time_value_in_minutes( scheduled_item.start_time )
   end_time = DateValues.time_value_in_minutes( scheduled_item.end_time )

   return ( start_time, end_time )


def schedule_times_overlap(
      first: ScheduledItem,
      second: ScheduledItem ) -> bool:
   first_start, first_end = schedule_time_range( first )
   second_start, second_end = schedule_time_range( second )

   return first_start < second_end and second_start < first_end


def active_scheduled_items(
      guardians_talks: list[ GuardiansTalkDiff ],
      wild_encounters: list[ WildEncounterDiff ],
) -> list[ ScheduledItem ]:
   active_talks = [
      guardians_talk
      for guardians_talk in guardians_talks
      if not guardians_talk.is_deleted
   ]
   active_encounters = [
      wild_encounter
      for wild_encounter in wild_encounters
      if not wild_encounter.is_deleted
   ]

   return active_talks + active_encounters


def collect_overlapping_group(
      scheduled_items: list[ ScheduledItem ],
      start_index: int,
      visited: set[ int ],
) -> list[ ScheduledItem ]:
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
      scheduled_items: list[ ScheduledItem ],
) -> list[ list[ ScheduledItem ] ]:
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
      scheduled_items: list[ ScheduledItem ],
) -> list[ ScheduledItem ]:
   return sorted(
      scheduled_items,
      key=lambda scheduled_item: (
         DateValues.time_value_in_minutes( scheduled_item.start_time )
         or 0,
         scheduled_item.name,
      ) )


def build_schedule_time_conflict_issue(
      scheduled_items: list[ ScheduledItem ],
) -> ItinerarySaveIssue:
   sorted_items = sort_scheduled_items_for_issue( scheduled_items )
   issue_items = tuple(
      scheduled_item_to_issue_item( scheduled_item )
      for scheduled_item in sorted_items
   )

   return ItinerarySaveIssue(
      issue_type=ItinerarySaveIssueType.WILD_ENCOUNTER_TIME_CONFLICT,
      items=issue_items )


def remove_scheduled_items_with_time_conflicts(
      guardians_talks: list[ GuardiansTalkDiff ],
      wild_encounters: list[ WildEncounterDiff ],
) -> tuple[
   list[ GuardiansTalkDiff ],
   list[ WildEncounterDiff ],
   tuple[ ItinerarySaveIssue, ... ],
]:
   scheduled_items = active_scheduled_items( guardians_talks, wild_encounters )
   conflict_groups = find_schedule_time_conflict_groups( scheduled_items )

   if not conflict_groups:
      return guardians_talks, wild_encounters, ()

   conflicting_talk_names = {
      scheduled_item.name
      for group in conflict_groups
      for scheduled_item in group
      if isinstance( scheduled_item, GuardiansTalkDiff )
   }
   conflicting_wild_encounter_names = {
      scheduled_item.name
      for group in conflict_groups
      for scheduled_item in group
      if isinstance( scheduled_item, WildEncounterDiff )
   }
   issues = [
      build_schedule_time_conflict_issue( group )
      for group in conflict_groups
   ]

   return (
      [
         guardians_talk
         for guardians_talk in guardians_talks
         if guardians_talk.name not in conflicting_talk_names
      ],
      [
         wild_encounter
         for wild_encounter in wild_encounters
         if wild_encounter.name not in conflicting_wild_encounter_names
      ],
      tuple( issues ),
   )


def remove_wild_encounters_with_time_conflicts(
      wild_encounters: list[ WildEncounterDiff ] ) -> tuple[
         list[ WildEncounterDiff ],
         tuple[ ItinerarySaveIssue, ... ],
      ]:
   filtered_wild_encounters, _, issues = remove_scheduled_items_with_time_conflicts(
      [],
      wild_encounters )

   return filtered_wild_encounters, issues
