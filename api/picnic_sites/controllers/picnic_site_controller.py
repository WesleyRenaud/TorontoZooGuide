from __future__ import annotations

from ... import zoo
from ..data_access.picnic_site import fetch_picnic_sites
from ...request_connection import get_connection


class PicnicSiteController():


   @classmethod
   def get_picnic_sites( cls ) -> list[ zoo.PicnicSite ]:
      return fetch_picnic_sites( get_connection() )
