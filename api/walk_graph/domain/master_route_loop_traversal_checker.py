from __future__ import annotations

from .master_route_loop import MasterRouteTraversal
from .master_route_loop import TWO_WAY_LOOP_TRAVERSAL


class MasterRouteLoopTraversalChecker():
   @classmethod
   def is_two_way(
         cls,
         traversal: MasterRouteTraversal | None ) -> bool:
      return traversal == TWO_WAY_LOOP_TRAVERSAL
