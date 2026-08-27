from __future__ import annotations

from dataclasses import dataclass


@dataclass
class LoopScheduleWindowState:
   cursor_seconds: int
   current_node_id: str
   departure_side_cluster_id: str | None
