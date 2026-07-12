from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass
from typing import Any, Self

from ...shared.schedule_row_input import parse_schedule_rows
from ...shared.schedule_row_input import SCHEDULE_ROW_WEEKDAY_KEYS
from ...shared.schedule_row_input import ScheduleRowInput


GUARDIANS_TALK_SCHEDULE_WEEKDAY_KEYS = SCHEDULE_ROW_WEEKDAY_KEYS


@dataclass( frozen=True )
class GuardiansTalkScheduleRowInput:
   talk_time: str
   monday: bool
   tuesday: bool
   wednesday: bool
   thursday: bool
   friday: bool
   saturday: bool
   sunday: bool

   @classmethod
   def from_wire( cls, row: Mapping[ str, Any ] ) -> Self | None:
      parsed_row = ScheduleRowInput.from_wire( row )

      if parsed_row is None:
         return None

      return cls.from_schedule_row( parsed_row )


   @classmethod
   def from_schedule_row( cls, row: ScheduleRowInput ) -> Self:
      return cls(
         talk_time=row.time,
         monday=row.monday,
         tuesday=row.tuesday,
         wednesday=row.wednesday,
         thursday=row.thursday,
         friday=row.friday,
         saturday=row.saturday,
         sunday=row.sunday )


def parse_guardians_talk_schedule_rows(
      schedule_rows: list[ dict[ str, Any ] ] | None ) -> list[ GuardiansTalkScheduleRowInput ]:
   return [
      GuardiansTalkScheduleRowInput.from_schedule_row( row )
      for row in parse_schedule_rows( schedule_rows )
   ]
