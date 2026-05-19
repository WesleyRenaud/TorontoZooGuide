from ..data_access.defibrillator import fetch_defibrillators


class DefibrillatorController():
   def __init__( self, conn ):
      self._conn = conn


   def get_defibrillators( self ):
      return fetch_defibrillators( self._conn )
