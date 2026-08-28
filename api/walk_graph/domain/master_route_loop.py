from __future__ import annotations

from dataclasses import dataclass

from .master_route_stop import MasterRouteStop


MasterRouteTraversal = str

TWO_WAY_LOOP_TRAVERSAL = 'two_way'
ONE_WAY_LOOP_TRAVERSAL = 'one_way'


@dataclass( frozen=True )
class MasterRouteLoop:
   loop_id: str
   name: str
   traversal: MasterRouteTraversal
   viewing_spots: list[ MasterRouteStop ]
