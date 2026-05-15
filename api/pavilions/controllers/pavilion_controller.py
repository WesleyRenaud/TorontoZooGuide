from ..data_access.pavilion import fetch_pavilions


class PavilionController():
   def __init__( self, conn ):
      self._conn = conn


   def get_pavilions( self ):
      return fetch_pavilions( self._conn )
