from __future__ import annotations

from dataclasses import dataclass

from ...shared.enums import ScheduleItemKind


@dataclass( frozen=True )
class WalkRouteLeg:
   from_item_key: str
   to_item_key: str
   from_schedule_item_kind: ScheduleItemKind
   to_schedule_item_kind: ScheduleItemKind
   node_ids: list[ str ]

   def to_dict( self ) -> dict[ str, object ]:
      return {
         'from_item_key': self.from_item_key,
         'to_item_key': self.to_item_key,
         'from_schedule_item_kind': self.from_schedule_item_kind.value,
         'to_schedule_item_kind': self.to_schedule_item_kind.value,
         'node_ids': self.node_ids,
      }
