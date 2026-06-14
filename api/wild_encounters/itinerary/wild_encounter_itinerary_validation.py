from __future__ import annotations

from ...itinerary.data_access.itinerary_wild_encounter_record import ItineraryWildEncounterRecord
from ...itinerary.scheduling import schedule_wild_encounter_for_itinerary
from ...models import WildEncounter
from ...models import WildEncounterDiff
from ..scheduling.wild_encounter_schedule import find_wild_encounter_on_day_schedule


def build_wild_encounter_diff_for_visit_day(
      name: str,
      encounter: WildEncounter | None ) -> WildEncounterDiff:
   return schedule_wild_encounter_for_itinerary( name, encounter )


def _find_saved_wild_encounter_row(
      saved_rows: list[ ItineraryWildEncounterRecord ] | None,
      name: str ) -> ItineraryWildEncounterRecord | None:
   for row in saved_rows or []:
      if row.is_deleted:
         continue

      if row.wild_encounter == name:
         return row

   return None


def validate_wild_encounters_for_itinerary(
      wild_encounters_to_include: list[ str ] | None,
      day_schedule: list[ WildEncounter ],
      *,
      saved_wild_encounter_rows: list[ ItineraryWildEncounterRecord ] | None = None ) -> list[ WildEncounterDiff ]:
   diffs: list[ WildEncounterDiff ] = []

   for encounter_name in wild_encounters_to_include or []:
      encounter = find_wild_encounter_on_day_schedule(
         day_schedule,
         encounter_name )
      name = encounter.name if encounter is not None else encounter_name
      wild_encounter = build_wild_encounter_diff_for_visit_day( name, encounter )
      saved_row = _find_saved_wild_encounter_row(
         saved_wild_encounter_rows,
         name )

      if saved_row is not None:
         wild_encounter.start_time = saved_row.start_time
         wild_encounter.end_time = saved_row.end_time

      diffs.append( wild_encounter )

   return diffs
