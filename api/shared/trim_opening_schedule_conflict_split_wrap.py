from __future__ import annotations

from collections.abc import Callable
from datetime import date
from datetime import timedelta

from .opening_schedule_conflict_record import TConflict
from .opening_schedule_dates import format_opening_schedule_date
from ..types import Connection


def trim_opening_schedule_conflict_split_wrap(
      conn: Connection,
      conflict: TConflict,
      *,
      new_start_date: date,
      new_end_date: date,
      conflict_start_attr: str,
      conflict_end_attr: str,
      update_dates: Callable,
      insert_copy: Callable,
) -> None:
   update_dates(
      conn,
      conflict,
      start_date=getattr( conflict, conflict_start_attr ),
      end_date=format_opening_schedule_date(
         new_start_date - timedelta( days=1 ) ) )

   if new_end_date == date.max:
      return

   insert_copy(
      conn,
      conflict,
      start_date=format_opening_schedule_date(
         new_end_date + timedelta( days=1 ) ),
      end_date=getattr( conflict, conflict_end_attr ) )
