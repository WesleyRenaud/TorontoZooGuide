from __future__ import annotations

from typing import Any


class StubSearchCoordinator():
   instances: list[ StubSearchCoordinator ] = []


   def __init__( self, *, results: dict[ str, list ] ) -> None:
      self.results = results
      self.calls: list[ tuple[ str, dict[ str, Any ] ] ] = []
      StubSearchCoordinator.instances.append( self )


   def search( self, **kwargs: Any ) -> dict[ str, list ]:
      self.calls.append( ( 'search', kwargs ) )
      return self.results
