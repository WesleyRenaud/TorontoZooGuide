from __future__ import annotations

from ..data_access.emergency_intercom_provider import EmergencyIntercomProvider
from ...models import EmergencyIntercom
from ...request_connection import get_connection


class EmergencyIntercomCoordinator():
   @classmethod
   def get_emergency_intercoms( cls ) -> list[ EmergencyIntercom ]:
      return EmergencyIntercomProvider.fetch_emergency_intercoms( get_connection() )
