from __future__ import annotations

from typing import Any

from ...models import GuardiansTalk
from ...shared.map_schedule_occurrence_collapser import MapScheduleOccurrenceCollapser


class GuardiansTalkMapScheduleCollapser():
   @classmethod
   def collapse(
         cls,
         guardians_talks: list[ GuardiansTalk ] ) -> list[ dict[ str, Any ] ]:
      return MapScheduleOccurrenceCollapser.collapse(
         guardians_talks,
         group_key=lambda talk: ( talk.name, talk.location ),
         get_start_time=lambda talk: talk.start_time )
