from __future__ import annotations

from typing import Any

from api_test_support.coordinator_call import CoordinatorCall

from api.models.restroom import Restroom


class StubRestroomCoordinator():
   instances: list[ StubRestroomCoordinator ] = []
   default_success: bool = True
   restroom_names: list[ str ]
   closed_restroom_names: list[ str ]
   alert_restroom_names: list[ str ]
   restrooms: list[ Restroom ]
   calls: list[ CoordinatorCall ]
   closed: bool


   def __init__(
         self,
         *,
         restroom_names: list[ str ],
         closed_restroom_names: list[ str ],
         alert_restroom_names: list[ str ],
         restrooms: list[ Restroom ] ) -> None:
      self.restroom_names = restroom_names
      self.closed_restroom_names = closed_restroom_names
      self.alert_restroom_names = alert_restroom_names
      self.restrooms = restrooms
      self.calls = []
      self.closed = False
      StubRestroomCoordinator.instances.append( self )


   def close( self ) -> None:
      self.closed = True


   def get_restroom_names( self ) -> list[ str ]:
      self.calls.append( CoordinatorCall( 'get_restroom_names', {} ) )
      return list( self.restroom_names )


   def get_closed_restroom_options( self ) -> list[ str ]:
      self.calls.append( CoordinatorCall( 'get_closed_restroom_options', {} ) )
      return list( self.closed_restroom_names )


   def get_restroom_alert_options( self ) -> list[ str ]:
      self.calls.append( CoordinatorCall( 'get_restroom_alert_options', {} ) )
      return list( self.alert_restroom_names )


   def get_restrooms(
         self,
         *,
         day: int,
         month: str,
         year: int,
         include_closed_restrooms: bool = False ) -> list[ Restroom ]:
      self.calls.append(
         CoordinatorCall(
            'get_restrooms',
            {
               'day': day,
               'month': month,
               'year': year,
               'include_closed_restrooms': include_closed_restrooms,
            },
         )
      )
      return list( self.restrooms )


   def set_restroom_as_closed( self, **kwargs: Any ) -> bool:
      self.calls.append( CoordinatorCall( 'set_restroom_as_closed', kwargs ) )
      return StubRestroomCoordinator.default_success


   def set_restroom_as_open( self, **kwargs: Any ) -> bool:
      self.calls.append( CoordinatorCall( 'set_restroom_as_open', kwargs ) )
      return StubRestroomCoordinator.default_success


   def set_restroom_alert( self, **kwargs: Any ) -> bool:
      self.calls.append( CoordinatorCall( 'set_restroom_alert', kwargs ) )
      return StubRestroomCoordinator.default_success


   def remove_restroom_alert( self, **kwargs: Any ) -> bool:
      self.calls.append( CoordinatorCall( 'remove_restroom_alert', kwargs ) )
      return StubRestroomCoordinator.default_success
