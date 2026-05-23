from __future__ import annotations

from ... import zoo
from ..data_access.emergency_intercom import fetch_emergency_intercoms
from ...request_connection import get_connection


class EmergencyIntercomController():


   @classmethod
   def get_emergency_intercoms( cls ) -> list[ zoo.EmergencyIntercom ]:
      return fetch_emergency_intercoms( get_connection() )
