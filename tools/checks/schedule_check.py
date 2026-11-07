from __future__ import annotations

from dataclasses import dataclass


@dataclass( frozen=True )
class ScheduleCheck:
   note: str
   only_in_app: list[ str ]
   only_on_website: list[ str ]
   different_slots: list[ str ]
   windows: list[ str ]
