from __future__ import annotations

from dataclasses import dataclass


@dataclass( frozen=True )
class ScheduledWalkStop:
   start_seconds: int
   end_seconds: int
   walk_node_id: str
