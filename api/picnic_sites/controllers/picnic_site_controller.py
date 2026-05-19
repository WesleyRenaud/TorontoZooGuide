from ..data_access.picnic_site import fetch_picnic_sites


class PicnicSiteController():
   def __init__( self, conn ):
      self._conn = conn


   def get_picnic_sites( self ):
      return fetch_picnic_sites( self._conn )
