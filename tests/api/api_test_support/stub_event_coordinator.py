from __future__ import annotations

from typing import Any

from api_test_support.coordinator_call import CoordinatorCall

from api.models.event import Event


class StubEventCoordinator():
   instances: list[ StubEventCoordinator ] = []
   default_success: bool = True
   events: list[ Event ]
   calls: list[ CoordinatorCall ]
   closed: bool


   def __init__(
         self,
         *,
         events: list[ Event ] ) -> None:
      self.events = events
      self.calls = []
      self.closed = False
      StubEventCoordinator.instances.append( self )


   def close( self ) -> None:
      self.closed = True


   def get_events_for_visit_date(
         self,
         *,
         month: str,
         day: int,
         year: int ) -> list[ Event ]:
      self.calls.append(
         CoordinatorCall(
            'get_events_for_visit_date',
            {
               'month': month,
               'day': day,
               'year': year,
            },
         )
      )
      return list( self.events )


   def create_event( self, **kwargs: Any ) -> bool:
      self.calls.append( CoordinatorCall( 'create_event', kwargs ) )
      return StubEventCoordinator.default_success
