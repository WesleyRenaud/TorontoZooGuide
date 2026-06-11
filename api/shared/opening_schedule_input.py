from __future__ import annotations

from typing import Protocol
from typing import TypeVar

from ..types import DateKey


class OpeningScheduleInput( Protocol ):
   start_date: DateKey
   end_date: DateKey | None


TSchedule = TypeVar( 'TSchedule', bound=OpeningScheduleInput )
