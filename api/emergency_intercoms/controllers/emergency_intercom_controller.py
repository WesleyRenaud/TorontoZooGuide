from ..data_access.emergency_intercom import fetch_emergency_intercoms


class EmergencyIntercomController():
   def __init__( self, conn ):
      self._conn = conn


   def get_emergency_intercoms( self ):
      return fetch_emergency_intercoms( self._conn )
