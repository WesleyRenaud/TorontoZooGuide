from __future__ import annotations

from dataclasses import dataclass
from typing import ClassVar

from .timed_name_schedule_item_key import TimedNameScheduleItemKey


@dataclass( frozen=True, eq=False )
class WildEncounterScheduleItemKey( TimedNameScheduleItemKey ):
   NAME_FIELDS: ClassVar[ list[ str ] ] = [ 'wild_encounter', 'name' ]
   LABEL: ClassVar[ str ] = 'wild encounter'
