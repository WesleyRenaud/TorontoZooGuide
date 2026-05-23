from __future__ import annotations

from ... import zoo
from ..data_access.guest_service import fetch_guest_services
from ...request_connection import get_connection


class GuestServiceController():


   @classmethod
   def get_guest_services( cls ) -> list[ zoo.GuestService ]:
      return fetch_guest_services( get_connection() )
