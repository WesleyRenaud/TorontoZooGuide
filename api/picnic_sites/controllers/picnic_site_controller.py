from __future__ import annotations

from ..coordinators.picnic_site_coordinator import PicnicSiteCoordinator
from ...json_handler import JsonRequestHandler


class PicnicSiteController():


   @staticmethod
   def get_picnic_sites( handler: JsonRequestHandler ) -> None:
      picnic_sites = PicnicSiteCoordinator.get_picnic_sites()

      handler._write_json( {
         'picnic_sites': [ picnic_site.to_dict() for picnic_site in picnic_sites ],
      } )
