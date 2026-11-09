from __future__ import annotations

from api_test_support.coordinator_call import CoordinatorCall

from api.models.defibrillator import Defibrillator


class StubDefibrillatorCoordinator():
   instances: list[ StubDefibrillatorCoordinator ] = []
   defibrillators: list[ Defibrillator ]
   calls: list[ CoordinatorCall ]


   def __init__( self, *, defibrillators: list[ Defibrillator ] ) -> None:
      self.defibrillators = defibrillators
      self.calls = []
      StubDefibrillatorCoordinator.instances.append( self )


   def get_defibrillators( self ) -> list[ Defibrillator ]:
      self.calls.append( CoordinatorCall( 'get_defibrillators', {} ) )
      return list( self.defibrillators )
