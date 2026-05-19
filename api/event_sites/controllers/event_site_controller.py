from ..data_access.event_site import fetch_event_sites


class EventSiteController():
   def __init__( self, conn ):
      self._conn = conn


   def get_event_sites( self ):
      return fetch_event_sites( self._conn )
