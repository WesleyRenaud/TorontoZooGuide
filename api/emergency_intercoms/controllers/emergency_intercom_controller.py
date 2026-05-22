from ..data_access.emergency_intercom import fetch_emergency_intercoms
from ...request_connection import get_connection


class EmergencyIntercomController():


   @classmethod
   def get_emergency_intercoms( cls ):
      return fetch_emergency_intercoms( get_connection() )
