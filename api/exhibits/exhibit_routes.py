from __future__ import annotations

from .controllers.exhibit_controller import ExhibitController
from ..json_request_handler import PostRouteHandler


class ExhibitRoutes():
   ROUTES: dict[ str, PostRouteHandler ] = {
   '/get-exhibits-in-region': ExhibitController.get_exhibits_in_region,
   '/get-regions': ExhibitController.get_regions,
   '/get-animal-names-by-exhibit': ExhibitController.get_animal_names_by_exhibit,
   '/get-closed-exhibits': ExhibitController.get_closed_exhibits,
   '/get-exhibits-by-region': ExhibitController.get_exhibits_by_region,
   '/get-exhibits': ExhibitController.get_exhibits,
   '/set-exhibit-closed': ExhibitController.set_exhibit_closed,
   '/set-exhibit-open': ExhibitController.set_exhibit_open,
}

