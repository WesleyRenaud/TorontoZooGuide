from __future__ import annotations

from typing import Protocol
from typing import TypeVar

from ..types import DateKey


class OpeningScheduleConflictRecord( Protocol ):
   schedule_start_date: DateKey
   schedule_end_date: DateKey | None


TConflict = TypeVar( 'TConflict', bound=OpeningScheduleConflictRecord )
