from __future__ import annotations

from ..data_access.guest_service_provider import GuestServiceProvider
from ...models import GuestService
from ...request_connection_provider import RequestConnectionProvider


class GuestServiceCoordinator():
   @classmethod
   def get_guest_services( cls ) -> list[ GuestService ]:
      return GuestServiceProvider.fetch_guest_services( RequestConnectionProvider.get() )
