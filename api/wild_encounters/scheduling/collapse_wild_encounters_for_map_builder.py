from __future__ import annotations

from typing import Any

from ...models import WildEncounter
from ...shared.map_schedule_occurrence_collapser import MapScheduleOccurrenceCollapser


class CollapseWildEncountersForMapBuilder():
   @classmethod
   def build(
         cls,
         wild_encounters: list[ WildEncounter ] ) -> list[ dict[ str, Any ] ]:
      return MapScheduleOccurrenceCollapser.collapse(
         wild_encounters,
         group_key=lambda encounter: encounter.name,
         get_start_time=lambda encounter: encounter.start_time )
