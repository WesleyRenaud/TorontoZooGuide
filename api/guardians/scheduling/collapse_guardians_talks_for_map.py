from __future__ import annotations

from typing import Any

from ...models import GuardiansTalk
from ...shared.collapse_map_schedule_occurrences import collapse_map_schedule_occurrences


def collapse_guardians_talks_for_map(
      guardians_talks: list[ GuardiansTalk ] ) -> list[ dict[ str, Any ] ]:
   return collapse_map_schedule_occurrences(
      guardians_talks,
      group_key=lambda talk: ( talk.name, talk.location ),
      get_start_time=lambda talk: talk.start_time )
