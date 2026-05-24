from __future__ import annotations

from .itinerary_save_issue import ItinerarySaveIssue
from .itinerary_save_issue_item import ItinerarySaveIssueItem
from ...models.wild_encounter_diff import WildEncounterDiff
from ...shared.date_values import DateValues
from ...shared.enums import ItinerarySaveIssueType
from ...shared.strings import SharedStrings


def wild_encounter_time_range(
      wild_encounter: WildEncounterDiff ) -> tuple[ int, int ]:
   start_time = DateValues.time_value_in_minutes( wild_encounter.start_time )
   end_time = DateValues.time_value_in_minutes( wild_encounter.end_time )

   return ( start_time, end_time )


def wild_encounter_times_overlap(
      first: WildEncounterDiff,
      second: WildEncounterDiff ) -> bool:
   first_start, first_end = wild_encounter_time_range( first )
   second_start, second_end = wild_encounter_time_range( second )

   return first_start < second_end and second_start < first_end


def build_wild_encounter_time_conflict_issue(
      first: WildEncounterDiff,
      second: WildEncounterDiff ) -> ItinerarySaveIssue:
   return ItinerarySaveIssue(
      issue_type=ItinerarySaveIssueType.WILD_ENCOUNTER_TIME_CONFLICT,
      message=SharedStrings.WildEncounters.time_conflict(
         first.name,
         second.name ),
      items=(
         ItinerarySaveIssueItem.from_wild_encounter_diff( first ),
         ItinerarySaveIssueItem.from_wild_encounter_diff( second ),
      ) )


def remove_wild_encounters_with_time_conflicts(
      wild_encounters: list[ WildEncounterDiff ] ) -> tuple[
         list[ WildEncounterDiff ],
         tuple[ ItinerarySaveIssue, ... ],
      ]:
   conflicting_names: set[ str ] = set()
   issues: list[ ItinerarySaveIssue ] = []

   for index, wild_encounter in enumerate( wild_encounters ):
      for other_wild_encounter in wild_encounters[ index + 1: ]:
         if wild_encounter.is_deleted or other_wild_encounter.is_deleted:
            continue

         if not wild_encounter_times_overlap(
               wild_encounter,
               other_wild_encounter ):
            continue

         conflicting_names.add( wild_encounter.name )
         conflicting_names.add( other_wild_encounter.name )
         issues.append(
            build_wild_encounter_time_conflict_issue(
               wild_encounter,
               other_wild_encounter ) )

   if not conflicting_names:
      return wild_encounters, ()

   return (
      [
         wild_encounter
         for wild_encounter in wild_encounters
         if wild_encounter.name not in conflicting_names
      ],
      tuple( issues ),
   )
