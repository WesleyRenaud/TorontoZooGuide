from __future__ import annotations

from dataclasses import dataclass

from .loop_schedule_stop import LoopScheduleStop


@dataclass( frozen=True )
class LoopScheduleUnit:
   loop_id: str | None
   stops: list[ LoopScheduleStop.Stop ]
   entry_walk_node_id: str | None
   exit_walk_node_id: str | None
   side_cluster_id: str | None
   loop_index_in_side_cluster: int | None
   traversal: str | None
