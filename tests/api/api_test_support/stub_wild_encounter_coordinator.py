from __future__ import annotations

from typing import Any

from api.models.scheduled_occurrence import ScheduledOccurrence
from api.models.wild_encounter import WildEncounter


class StubWildEncounterCoordinator():
   instances: list[ StubWildEncounterCoordinator ] = []
   default_success: bool = True


   def __init__(
         self,
         *,
         wild_encounters: list[ WildEncounter ],
         wild_encounter_names: list[ str ],
         wild_encounter_occurrences: list[ ScheduledOccurrence ],
         wild_encounter_schedule_times: list[ str ] ) -> None:
      self.wild_encounters = wild_encounters
      self.wild_encounter_names = wild_encounter_names
      self.wild_encounter_occurrences = wild_encounter_occurrences
      self.wild_encounter_schedule_times = wild_encounter_schedule_times
      self.calls: list[ tuple[ str, dict[ str, Any ] ] ] = []
      self.closed = False
      StubWildEncounterCoordinator.instances.append( self )


   def close( self ) -> None:
      self.closed = True


   def get_available_wild_encounters(
         self,
         *,
         month: str,
         day: int,
         year: int ) -> list[ WildEncounter ]:
      self.calls.append(
         (
            'get_available_wild_encounters',
            {
               'month': month,
               'day': day,
               'year': year,
            }
         )
      )
      return list( self.wild_encounters )


   def get_wild_encounter_names( self ) -> list[ str ]:
      self.calls.append( ( 'get_wild_encounter_names', {} ) )
      return list( self.wild_encounter_names )


   def get_wild_encounter_occurrences(
         self,
         *,
         wild_encounter_name: str ) -> list[ ScheduledOccurrence ]:
      self.calls.append(
         (
            'get_wild_encounter_occurrences',
            { 'wild_encounter_name': wild_encounter_name },
         )
      )
      return list( self.wild_encounter_occurrences )


   def set_wild_encounter_schedule( self, **kwargs: Any ) -> bool:
      self.calls.append( ( 'set_wild_encounter_schedule', kwargs ) )
      return StubWildEncounterCoordinator.default_success


   def replace_wild_encounter_schedule_overlaps( self, **kwargs: Any ) -> bool:
      self.calls.append( ( 'replace_wild_encounter_schedule_overlaps', kwargs ) )
      return StubWildEncounterCoordinator.default_success


   def trim_wild_encounter_schedule_overlaps( self, **kwargs: Any ) -> bool:
      self.calls.append( ( 'trim_wild_encounter_schedule_overlaps', kwargs ) )
      return StubWildEncounterCoordinator.default_success


   def get_wild_encounter_schedule_times(
         self,
         *,
         wild_encounter_name: str ) -> list[ str ]:
      self.calls.append(
         (
            'get_wild_encounter_schedule_times',
            { 'wild_encounter_name': wild_encounter_name },
         )
      )
      return list( self.wild_encounter_schedule_times )


   def end_wild_encounter_schedule( self, **kwargs: Any ) -> bool:
      self.calls.append( ( 'end_wild_encounter_schedule', kwargs ) )
      return StubWildEncounterCoordinator.default_success


   def cancel_wild_encounter_occurrence( self, **kwargs: Any ) -> bool:
      self.calls.append( ( 'cancel_wild_encounter_occurrence', kwargs ) )
      return StubWildEncounterCoordinator.default_success
