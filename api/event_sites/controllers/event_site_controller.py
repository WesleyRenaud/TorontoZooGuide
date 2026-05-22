from ..data_access.event_site import fetch_event_sites
from ...request_connection import get_connection


class EventSiteController():


   @classmethod
   def get_event_sites( cls ):
      return fetch_event_sites( get_connection() )
