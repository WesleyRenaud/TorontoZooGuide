from __future__ import annotations

from api_test_support.coordinator_call import CoordinatorCall

from api.models.guest_service import GuestService


class StubGuestServiceCoordinator():
   instances: list[ StubGuestServiceCoordinator ] = []
   guest_services: list[ GuestService ]
   calls: list[ CoordinatorCall ]


   def __init__( self, *, guest_services: list[ GuestService ] ) -> None:
      self.guest_services = guest_services
      self.calls = []
      StubGuestServiceCoordinator.instances.append( self )


   def get_guest_services( self ) -> list[ GuestService ]:
      self.calls.append( CoordinatorCall( 'get_guest_services', {} ) )
      return list( self.guest_services )
