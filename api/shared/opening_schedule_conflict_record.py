from __future__ import annotations

from typing import Protocol
from typing import TypeVar

from ..types import Types


class OpeningScheduleConflictRecord( Protocol ):
   schedule_start_date: Types.DateKey
   schedule_end_date: Types.DateKey | None


TConflict = TypeVar( 'TConflict', bound=OpeningScheduleConflictRecord )
