from __future__ import annotations

from typing import Any

from api_test_support.coordinator_call import CoordinatorCall

from api.guardians.domain.guardians_talk_option import GuardiansTalkOption
from api.models.guardians_talk import GuardiansTalk
from api.models.scheduled_occurrence import ScheduledOccurrence
from api.shared.api_operation_failure import ApiOperationFailure


class StubGuardiansCoordinator():
   instances: list[ StubGuardiansCoordinator ] = []
   default_success: bool = True
   default_failure: ApiOperationFailure | None = None
   guardians_talks: list[ GuardiansTalk ]
   guardians_talk_locations: list[ str ]
   guardians_talk_names: list[ str ]
   guardians_talk_names_at_location: list[ GuardiansTalkOption ]
   guardians_talk_occurrences: list[ ScheduledOccurrence ]
   guardians_talk_schedule_times: list[ str ]
   calls: list[ CoordinatorCall ]
   closed: bool


   def __init__(
         self,
         *,
         guardians_talks: list[ GuardiansTalk ],
         guardians_talk_locations: list[ str ],
         guardians_talk_names: list[ str ],
         guardians_talk_names_at_location: list[ GuardiansTalkOption ],
         guardians_talk_occurrences: list[ ScheduledOccurrence ],
         guardians_talk_schedule_times: list[ str ] ) -> None:
      self.guardians_talks = guardians_talks
      self.guardians_talk_locations = guardians_talk_locations
      self.guardians_talk_names = guardians_talk_names
      self.guardians_talk_names_at_location = guardians_talk_names_at_location
      self.guardians_talk_occurrences = guardians_talk_occurrences
      self.guardians_talk_schedule_times = guardians_talk_schedule_times
      self.calls = []
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
         CoordinatorCall(
            'get_guardians_talk_schedule',
            {
               'month': month,
               'day': day,
               'year': year,
            },
         )
      )
      return list( self.guardians_talks )


   def get_guardians_talk_locations( self ) -> list[ str ]:
      self.calls.append( CoordinatorCall( 'get_guardians_talk_locations', {} ) )
      return list( self.guardians_talk_locations )


   def get_guardians_talk_names( self ) -> list[ str ]:
      self.calls.append( CoordinatorCall( 'get_guardians_talk_names', {} ) )
      return list( self.guardians_talk_names )


   def get_guardians_talk_names_at_location(
         self,
         *,
         location: str ) -> list[ GuardiansTalkOption ]:
      self.calls.append(
         CoordinatorCall( 'get_guardians_talk_names_at_location', { 'location': location } )
      )
      return list( self.guardians_talk_names_at_location )


   def get_guardians_talk_schedule_options(
         self,
         *,
         location: str ) -> list[ GuardiansTalkOption ]:
      self.calls.append(
         CoordinatorCall( 'get_guardians_talk_schedule_options', { 'location': location } )
      )
      return list( self.guardians_talk_names_at_location )


   def get_guardians_talk_schedule_location_options( self ) -> list[ str ]:
      self.calls.append( CoordinatorCall( 'get_guardians_talk_schedule_location_options', {} ) )
      return list( self.guardians_talk_locations )


   def get_guardians_talk_occurrences(
         self,
         *,
         talk: str,
         location: str,
         enclosure_name: str ) -> list[ ScheduledOccurrence ]:
      self.calls.append(
         CoordinatorCall(
            'get_guardians_talk_occurrences',
            {
               'talk': talk,
               'location': location,
               'enclosure_name': enclosure_name,
            },
         )
      )
      return list( self.guardians_talk_occurrences )


   def set_guardians_talk_schedule( self, **kwargs: Any ) -> bool:
      self.calls.append( CoordinatorCall( 'set_guardians_talk_schedule', kwargs ) )
      return StubGuardiansCoordinator.default_success


   def replace_guardians_talk_schedule_overlaps( self, **kwargs: Any ) -> bool:
      self.calls.append( CoordinatorCall( 'replace_guardians_talk_schedule_overlaps', kwargs ) )
      return StubGuardiansCoordinator.default_success


   def trim_guardians_talk_schedule_overlaps( self, **kwargs: Any ) -> bool:
      self.calls.append( CoordinatorCall( 'trim_guardians_talk_schedule_overlaps', kwargs ) )
      return StubGuardiansCoordinator.default_success


   def get_guardians_talk_schedule_times(
         self,
         *,
         talk: str,
         location: str,
         enclosure_name: str ) -> list[ str ]:
      self.calls.append(
         CoordinatorCall(
            'get_guardians_talk_schedule_times',
            {
               'talk': talk,
               'location': location,
               'enclosure_name': enclosure_name,
            },
         )
      )
      return list( self.guardians_talk_schedule_times )


   def end_guardians_talk_schedule( self, **kwargs: Any ) -> bool:
      self.calls.append( CoordinatorCall( 'end_guardians_talk_schedule', kwargs ) )
      return StubGuardiansCoordinator.default_success


   def cancel_guardians_talk_occurrence( self, **kwargs: Any ) -> bool:
      self.calls.append( CoordinatorCall( 'cancel_guardians_talk_occurrence', kwargs ) )
      return StubGuardiansCoordinator.default_success


   def add_guardians_talk_occurrence(
         self,
         **kwargs: Any ) -> tuple[ bool, ApiOperationFailure | None ]:
      self.calls.append( CoordinatorCall( 'add_guardians_talk_occurrence', kwargs ) )

      if StubGuardiansCoordinator.default_failure is not None:
         return ( False, StubGuardiansCoordinator.default_failure )

      return ( StubGuardiansCoordinator.default_success, None )
