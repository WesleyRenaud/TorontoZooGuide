from __future__ import annotations

from api.models.pavilion import Pavilion


class StubPavilionCoordinator():
   instances: list[ StubPavilionCoordinator ] = []


   def __init__( self, *, pavilions: list[ Pavilion ] ) -> None:
      self.pavilions = pavilions
      self.calls: list[ tuple[ str, dict[ str, object ] ] ] = []
      StubPavilionCoordinator.instances.append( self )


   def get_pavilions( self ) -> list[ Pavilion ]:
      self.calls.append( ( 'get_pavilions', {} ) )
      return list( self.pavilions )
