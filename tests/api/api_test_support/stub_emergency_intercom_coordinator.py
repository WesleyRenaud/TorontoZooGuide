from __future__ import annotations

from api_test_support.coordinator_call import CoordinatorCall

from api.models.emergency_intercom import EmergencyIntercom


class StubEmergencyIntercomCoordinator():
   instances: list[ StubEmergencyIntercomCoordinator ] = []
   emergency_intercoms: list[ EmergencyIntercom ]
   calls: list[ CoordinatorCall ]


   def __init__( self, *, emergency_intercoms: list[ EmergencyIntercom ] ) -> None:
      self.emergency_intercoms = emergency_intercoms
      self.calls = []
      StubEmergencyIntercomCoordinator.instances.append( self )


   def get_emergency_intercoms( self ) -> list[ EmergencyIntercom ]:
      self.calls.append( CoordinatorCall( 'get_emergency_intercoms', {} ) )
      return list( self.emergency_intercoms )
