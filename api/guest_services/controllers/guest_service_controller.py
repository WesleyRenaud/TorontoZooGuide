from ..data_access.guest_service import fetch_guest_services


class GuestServiceController():
   def __init__( self, conn ):
      self._conn = conn


   def get_guest_services( self ):
      return fetch_guest_services( self._conn )
