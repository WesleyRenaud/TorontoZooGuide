from __future__ import annotations

from ..data_access.emergency_intercom_provider import EmergencyIntercomProvider
from ...models import EmergencyIntercom
from ...request_connection_provider import RequestConnectionProvider


class EmergencyIntercomCoordinator():
   @classmethod
   def get_emergency_intercoms( cls ) -> list[ EmergencyIntercom ]:
      return EmergencyIntercomProvider.fetch_emergency_intercoms( RequestConnectionProvider.get() )
