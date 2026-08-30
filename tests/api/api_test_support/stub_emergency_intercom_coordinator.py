from __future__ import annotations

from api.models.emergency_intercom import EmergencyIntercom


class StubEmergencyIntercomCoordinator():
   instances: list[ StubEmergencyIntercomCoordinator ] = []


   def __init__( self, *, emergency_intercoms: list[ EmergencyIntercom ] ) -> None:
      self.emergency_intercoms = emergency_intercoms
      self.calls: list[ tuple[ str, dict[ str, object ] ] ] = []
      StubEmergencyIntercomCoordinator.instances.append( self )


   def get_emergency_intercoms( self ) -> list[ EmergencyIntercom ]:
      self.calls.append( ( 'get_emergency_intercoms', {} ) )
      return list( self.emergency_intercoms )
