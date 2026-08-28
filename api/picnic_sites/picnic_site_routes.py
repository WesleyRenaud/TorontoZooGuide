from __future__ import annotations

from .controllers.picnic_site_controller import PicnicSiteController
from ..json_request_handler import PostRouteHandler


class PicnicSiteRoutes():
   ROUTES: dict[ str, PostRouteHandler ] = {
   '/get-picnic-sites': PicnicSiteController.get_picnic_sites,
}

