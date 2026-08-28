from __future__ import annotations

from .attraction_route_stop import AttractionRouteStop
from .viewing_spot_reference import ViewingSpotReference


MasterRouteStop = ViewingSpotReference | AttractionRouteStop
