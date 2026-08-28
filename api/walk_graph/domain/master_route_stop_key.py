from __future__ import annotations

from typing import TypeAlias

from .animal_master_route_stop_key import AnimalMasterRouteStopKey
from .attraction_master_route_stop_key import AttractionMasterRouteStopKey


class MasterRouteStopKey():
   Key: TypeAlias = AnimalMasterRouteStopKey.Key | AttractionMasterRouteStopKey.Key
