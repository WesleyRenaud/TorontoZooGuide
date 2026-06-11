from __future__ import annotations

from collections.abc import Callable

from .date_values import DateValues
from .opening_schedule_conflict_record import TConflict
from .opening_schedule_dates import parse_opening_schedule_end_date
from .opening_schedule_input import TSchedule
from .trim_opening_schedule_conflict_delete_enclosed import try_trim_opening_schedule_conflict_delete_enclosed
from .trim_opening_schedule_conflict_shorten_end import try_trim_opening_schedule_conflict_shorten_end
from .trim_opening_schedule_conflict_shorten_start import try_trim_opening_schedule_conflict_shorten_start
from .trim_opening_schedule_conflict_split_wrap import trim_opening_schedule_conflict_split_wrap
from ..types import Connection


def trim_opening_schedule_conflict(
      conn: Connection,
      conflict: TConflict,
      schedule: TSchedule,
      *,
      delete_conflict: Callable,
      update_dates: Callable,
      insert_copy: Callable,
      conflict_start_attr: str = 'schedule_start_date',
      conflict_end_attr: str = 'schedule_end_date',
      new_start_attr: str = 'start_date',
      new_end_attr: str = 'end_date',
) -> None:
   new_start_date = DateValues.parse_date_value(
      getattr( schedule, new_start_attr ) )
   new_end_date = parse_opening_schedule_end_date(
      getattr( schedule, new_end_attr ) )
   conflict_start_date = DateValues.parse_date_value(
      getattr( conflict, conflict_start_attr ) )
   conflict_end_date = parse_opening_schedule_end_date(
      getattr( conflict, conflict_end_attr ) )

   if try_trim_opening_schedule_conflict_delete_enclosed(
         conn,
         conflict,
         conflict_start_date=conflict_start_date,
         conflict_end_date=conflict_end_date,
         new_start_date=new_start_date,
         new_end_date=new_end_date,
         delete_conflict=delete_conflict ):
      return

   if try_trim_opening_schedule_conflict_shorten_end(
         conn,
         conflict,
         conflict_start_date=conflict_start_date,
         conflict_end_date=conflict_end_date,
         new_start_date=new_start_date,
         new_end_date=new_end_date,
         conflict_start_attr=conflict_start_attr,
         update_dates=update_dates ):
      return

   if try_trim_opening_schedule_conflict_shorten_start(
         conn,
         conflict,
         conflict_start_date=conflict_start_date,
         conflict_end_date=conflict_end_date,
         new_start_date=new_start_date,
         new_end_date=new_end_date,
         conflict_end_attr=conflict_end_attr,
         update_dates=update_dates ):
      return

   trim_opening_schedule_conflict_split_wrap(
      conn,
      conflict,
      new_start_date=new_start_date,
      new_end_date=new_end_date,
      conflict_start_attr=conflict_start_attr,
      conflict_end_attr=conflict_end_attr,
      update_dates=update_dates,
      insert_copy=insert_copy )


def save_opening_schedule_replacing_overlaps(
      conn: Connection,
      schedule: TSchedule,
      *,
      fetch_conflicts: Callable,
      delete_conflict: Callable,
      insert_or_update: Callable,
) -> bool:
   conflicts = fetch_conflicts( conn, schedule )

   for conflict in conflicts:
      delete_conflict( conn, conflict )

   insert_or_update( conn, schedule )
   conn.commit()
   return True


def save_opening_schedule_trimming_overlaps(
      conn: Connection,
      schedule: TSchedule,
      *,
      fetch_conflicts: Callable,
      trim_conflict: Callable,
      insert_or_update: Callable,
) -> bool:
   conflicts = fetch_conflicts( conn, schedule )

   for conflict in conflicts:
      trim_conflict( conn, conflict, schedule )

   insert_or_update( conn, schedule )
   conn.commit()
   return True
