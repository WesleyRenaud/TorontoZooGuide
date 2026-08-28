from __future__ import annotations

from typing import Any

from api.models.guardians_talk import GuardiansTalk
from api.models.scheduled_occurrence import ScheduledOccurrence
from api.shared.api_operation_failure import ApiOperationFailure


class StubGuardiansCoordinator():
   instances: list[ StubGuardiansCoordinator ] = []
   default_success: bool = True
   default_failure: ApiOperationFailure | None = None


   def __init__(
         self,
         *,
         guardians_talks: list[ GuardiansTalk ],
         guardians_talk_locations: list[ str ],
         guardians_talk_names: list[ str ],
         guardians_talk_names_at_location: list[ str ],
         guardians_talk_occurrences: list[ ScheduledOccurrence ],
         guardians_talk_schedule_times: list[ str ] ) -> None:
      self.guardians_talks = guardians_talks
      self.guardians_talk_locations = guardians_talk_locations
      self.guardians_talk_names = guardians_talk_names
      self.guardians_talk_names_at_location = guardians_talk_names_at_location
      self.guardians_talk_occurrences = guardians_talk_occurrences
      self.guardians_talk_schedule_times = guardians_talk_schedule_times
      self.calls: list[ tuple[ str, dict[ str, Any ] ] ] = []
      self.closed = False
      StubGuardiansCoordinator.instances.append( self )


   def close( self ) -> None:
      self.closed = True


   def get_guardians_talk_schedule(
         self,
         *,
         month: str,
         day: int,
         year: int ) -> list[ GuardiansTalk ]:
      self.calls.append(
         (
            'get_guardians_talk_schedule',
            {
               'month': month,
               'day': day,
               'year': year,
            }
         )
      )
      return list( self.guardians_talks )


   def get_guardians_talk_locations( self ) -> list[ str ]:
      self.calls.append( ( 'get_guardians_talk_locations', {} ) )
      return list( self.guardians_talk_locations )


   def get_guardians_talk_names( self ) -> list[ str ]:
      self.calls.append( ( 'get_guardians_talk_names', {} ) )
      return list( self.guardians_talk_names )


   def get_guardians_talk_names_at_location(
         self,
         *,
         location: str ) -> list[ str ]:
      self.calls.append(
         (
            'get_guardians_talk_names_at_location',
            { 'location': location },
         )
      )
      return list( self.guardians_talk_names_at_location )


   def get_guardians_talk_occurrences(
         self,
         *,
         talk: str,
         location: str ) -> list[ ScheduledOccurrence ]:
      self.calls.append(
         (
            'get_guardians_talk_occurrences',
            {
               'talk': talk,
               'location': location,
            }
         )
      )
      return list( self.guardians_talk_occurrences )


   def set_guardians_talk_schedule( self, **kwargs: Any ) -> bool:
      self.calls.append( ( 'set_guardians_talk_schedule', kwargs ) )
      return StubGuardiansCoordinator.default_success


   def replace_guardians_talk_schedule_overlaps( self, **kwargs: Any ) -> bool:
      self.calls.append( ( 'replace_guardians_talk_schedule_overlaps', kwargs ) )
      return StubGuardiansCoordinator.default_success


   def trim_guardians_talk_schedule_overlaps( self, **kwargs: Any ) -> bool:
      self.calls.append( ( 'trim_guardians_talk_schedule_overlaps', kwargs ) )
      return StubGuardiansCoordinator.default_success


   def get_guardians_talk_schedule_times(
         self,
         *,
         talk: str,
         location: str ) -> list[ str ]:
      self.calls.append(
         (
            'get_guardians_talk_schedule_times',
            {
               'talk': talk,
               'location': location,
            }
         )
      )
      return list( self.guardians_talk_schedule_times )


   def end_guardians_talk_schedule( self, **kwargs: Any ) -> bool:
      self.calls.append( ( 'end_guardians_talk_schedule', kwargs ) )
      return StubGuardiansCoordinator.default_success


   def cancel_guardians_talk_occurrence( self, **kwargs: Any ) -> bool:
      self.calls.append( ( 'cancel_guardians_talk_occurrence', kwargs ) )
      return StubGuardiansCoordinator.default_success


   def add_guardians_talk_occurrence(
         self,
         **kwargs: Any ) -> tuple[ bool, ApiOperationFailure | None ]:
      self.calls.append( ( 'add_guardians_talk_occurrence', kwargs ) )

      if StubGuardiansCoordinator.default_failure is not None:
         return ( False, StubGuardiansCoordinator.default_failure )

      return ( StubGuardiansCoordinator.default_success, None )
