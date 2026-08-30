from __future__ import annotations

from api.models.guest_service import GuestService


class StubGuestServiceCoordinator():
   instances: list[ StubGuestServiceCoordinator ] = []


   def __init__( self, *, guest_services: list[ GuestService ] ) -> None:
      self.guest_services = guest_services
      self.calls: list[ tuple[ str, dict[ str, object ] ] ] = []
      StubGuestServiceCoordinator.instances.append( self )


   def get_guest_services( self ) -> list[ GuestService ]:
      self.calls.append( ( 'get_guest_services', {} ) )
      return list( self.guest_services )
