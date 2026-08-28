from __future__ import annotations

from typing import Any

from api.models.update import Update


class StubUpdateCoordinator():
   instances: list[ StubUpdateCoordinator ] = []
   default_success: bool = True


   def __init__(
         self,
         *,
         updates: list[ Update ],
         active_updates: list[ Update ] ) -> None:
      self.updates = updates
      self.active_updates = active_updates
      self.calls: list[ tuple[ str, dict[ str, Any ] ] ] = []
      self.closed = False
      StubUpdateCoordinator.instances.append( self )


   def close( self ) -> None:
      self.closed = True


   def get_updates_for_visit_date(
         self,
         *,
         month: str,
         day: int,
         year: int ) -> list[ Update ]:
      self.calls.append(
         (
            'get_updates_for_visit_date',
            {
               'month': month,
               'day': day,
               'year': year,
            }
         )
      )
      return list( self.updates )


   def get_unexpired_updates( self ) -> list[ Update ]:
      self.calls.append( ( 'get_unexpired_updates', {} ) )
      return list( self.active_updates )


   def create_update( self, **kwargs: Any ) -> bool:
      self.calls.append( ( 'create_update', kwargs ) )
      return StubUpdateCoordinator.default_success


   def end_update( self, **kwargs: Any ) -> bool:
      self.calls.append( ( 'end_update', kwargs ) )
      return StubUpdateCoordinator.default_success


   def edit_update( self, **kwargs: Any ) -> bool:
      self.calls.append( ( 'edit_update', kwargs ) )
      return StubUpdateCoordinator.default_success
