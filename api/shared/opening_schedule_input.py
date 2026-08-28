from __future__ import annotations

from typing import Protocol
from typing import TypeVar

from ..types import Types


class OpeningScheduleInput( Protocol ):
   start_date: Types.DateKey
   end_date: Types.DateKey | None


TSchedule = TypeVar( 'TSchedule', bound=OpeningScheduleInput )
