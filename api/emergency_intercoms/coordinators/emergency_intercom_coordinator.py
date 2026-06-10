from __future__ import annotations

from ..data_access.emergency_intercom import fetch_emergency_intercoms
from ...models import EmergencyIntercom
from ...request_connection import get_connection


class EmergencyIntercomCoordinator():


   @classmethod
   def get_emergency_intercoms( cls ) -> list[ EmergencyIntercom ]:
      return fetch_emergency_intercoms( get_connection() )
