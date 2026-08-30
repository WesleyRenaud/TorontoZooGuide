from __future__ import annotations

from api.models.defibrillator import Defibrillator


class StubDefibrillatorCoordinator():
   instances: list[ StubDefibrillatorCoordinator ] = []


   def __init__( self, *, defibrillators: list[ Defibrillator ] ) -> None:
      self.defibrillators = defibrillators
      self.calls: list[ tuple[ str, dict[ str, object ] ] ] = []
      StubDefibrillatorCoordinator.instances.append( self )


   def get_defibrillators( self ) -> list[ Defibrillator ]:
      self.calls.append( ( 'get_defibrillators', {} ) )
      return list( self.defibrillators )
