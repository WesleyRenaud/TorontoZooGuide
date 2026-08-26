from __future__ import annotations

from typing import Any

from ...models import WildEncounter
from ...shared.collapse_map_schedule_occurrences import collapse_map_schedule_occurrences


class CollapseWildEncountersForMapBuilder():
   @classmethod
   def build(
         cls,
         wild_encounters: list[ WildEncounter ] ) -> list[ dict[ str, Any ] ]:
      return collapse_map_schedule_occurrences(
         wild_encounters,
         group_key=lambda encounter: encounter.name,
         get_start_time=lambda encounter: encounter.start_time )
