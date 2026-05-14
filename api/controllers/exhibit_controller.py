from ..data_access.exhibit import fetch_exhibit_names_in_region
from ..data_access.exhibit import fetch_region_exhibit_rows
from ..logic.exhibit import build_region_options


class ExhibitController():
   def __init__( self, conn ):
      self._conn = conn


   def get_exhibits_in_region( self, region ):
      return fetch_exhibit_names_in_region(
         self._conn,
         region=region )


   def get_regions( self ):
      return build_region_options(
         fetch_region_exhibit_rows( self._conn ) )
