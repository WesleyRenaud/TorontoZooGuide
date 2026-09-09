from __future__ import annotations

from dataclasses import dataclass
from typing import ClassVar

from .timed_name_schedule_item_key import TimedNameScheduleItemKey


@dataclass( frozen=True, eq=False )
class GuardiansTalkScheduleItemKey( TimedNameScheduleItemKey ):
   NAME_FIELDS: ClassVar[ list[ str ] ] = [ 'talk_name', 'name' ]
   LABEL: ClassVar[ str ] = 'guardians talk'
