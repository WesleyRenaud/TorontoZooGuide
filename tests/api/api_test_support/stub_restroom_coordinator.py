from __future__ import annotations

from typing import Any

from api.models.restroom import Restroom


class StubRestroomCoordinator():
   instances: list[ StubRestroomCoordinator ] = []
   default_success: bool = True


   def __init__(
         self,
         *,
         restroom_names: list[ str ],
         restrooms: list[ Restroom ] ) -> None:
      self.restroom_names = restroom_names
      self.restrooms = restrooms
      self.calls: list[ tuple[ str, dict[ str, Any ] ] ] = []
      self.closed = False
      StubRestroomCoordinator.instances.append( self )


   def close( self ) -> None:
      self.closed = True


   def get_restroom_names( self ) -> list[ str ]:
      self.calls.append( ( 'get_restroom_names', {} ) )
      return list( self.restroom_names )


   def get_restrooms(
         self,
         *,
         day: int,
         month: str,
         year: int,
         include_closed_restrooms: bool = False ) -> list[ Restroom ]:
      self.calls.append(
         (
            'get_restrooms',
            {
               'day': day,
               'month': month,
               'year': year,
               'include_closed_restrooms': include_closed_restrooms,
            }
         )
      )
      return list( self.restrooms )


   def set_restroom_as_closed( self, **kwargs: Any ) -> bool:
      self.calls.append( ( 'set_restroom_as_closed', kwargs ) )
      return StubRestroomCoordinator.default_success


   def set_restroom_as_open( self, **kwargs: Any ) -> bool:
      self.calls.append( ( 'set_restroom_as_open', kwargs ) )
      return StubRestroomCoordinator.default_success


   def set_restroom_alert( self, **kwargs: Any ) -> bool:
      self.calls.append( ( 'set_restroom_alert', kwargs ) )
      return StubRestroomCoordinator.default_success


   def remove_restroom_alert( self, **kwargs: Any ) -> bool:
      self.calls.append( ( 'remove_restroom_alert', kwargs ) )
      return StubRestroomCoordinator.default_success
