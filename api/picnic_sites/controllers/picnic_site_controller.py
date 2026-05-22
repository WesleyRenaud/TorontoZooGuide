from ..data_access.picnic_site import fetch_picnic_sites
from ...request_connection import get_connection


class PicnicSiteController():


   @classmethod
   def get_picnic_sites( cls ):
      return fetch_picnic_sites( get_connection() )
