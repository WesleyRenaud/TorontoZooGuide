from __future__ import annotations

from typing import Any

from api_test_support.coordinator_call import CoordinatorCall


class StubSearchCoordinator():
   instances: list[ StubSearchCoordinator ] = []
   results: dict[ str, list ]
   calls: list[ CoordinatorCall ]


   def __init__( self, *, results: dict[ str, list ] ) -> None:
      self.results = results
      self.calls = []
      StubSearchCoordinator.instances.append( self )


   def search( self, **kwargs: Any ) -> dict[ str, list ]:
      self.calls.append( CoordinatorCall( 'search', kwargs ) )
      return self.results
