from __future__ import annotations

from typing import TypeAlias

from .attraction_route_stop import AttractionRouteStop
from .viewing_spot_reference import ViewingSpotReference


class MasterRouteStop():
   Stop: TypeAlias = ViewingSpotReference | AttractionRouteStop
