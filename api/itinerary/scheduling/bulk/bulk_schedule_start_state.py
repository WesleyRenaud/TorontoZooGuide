from __future__ import annotations

from dataclasses import dataclass


@dataclass( frozen=True )
class BulkScheduleStartState:
   start_node_id: str
   schedule_anchor_seconds: int
