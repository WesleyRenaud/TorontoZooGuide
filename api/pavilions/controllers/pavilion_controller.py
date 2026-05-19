from ..data_access.pavilion import fetch_pavilions
from ..logic.pavilions_matching_query import build_pavilions_matching_query


class PavilionController():
   def __init__( self, conn ):
      self._conn = conn


   def get_pavilions( self ):
      return fetch_pavilions( self._conn )


   def get_pavilions_matching_query( self, query ):
      return build_pavilions_matching_query(
         self.get_pavilions(),
         query )
