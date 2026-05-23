from __future__ import annotations

from ...models import GuestService
from ..data_access.guest_service import fetch_guest_services
from ...request_connection import get_connection


class GuestServiceController():


   @classmethod
   def get_guest_services( cls ) -> list[ GuestService ]:
      return fetch_guest_services( get_connection() )
