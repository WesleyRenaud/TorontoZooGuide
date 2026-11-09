from __future__ import annotations

from api_test_support.coordinator_call import CoordinatorCall

from api.models.pavilion import Pavilion


class StubPavilionCoordinator():
   instances: list[ StubPavilionCoordinator ] = []
   pavilions: list[ Pavilion ]
   calls: list[ CoordinatorCall ]


   def __init__( self, *, pavilions: list[ Pavilion ] ) -> None:
      self.pavilions = pavilions
      self.calls = []
      StubPavilionCoordinator.instances.append( self )


   def get_pavilions( self ) -> list[ Pavilion ]:
      self.calls.append( CoordinatorCall( 'get_pavilions', {} ) )
      return list( self.pavilions )
