from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass
from typing import Any
from typing import Generic
from typing import TypeVar

from .constants import Constants
from .enums import AmenityNameField
from ..types import Types


TOpeningSchedule = TypeVar( 'TOpeningSchedule' )
TScheduleRecord = TypeVar( 'TScheduleRecord' )
TScheduleOverride = TypeVar( 'TScheduleOverride' )


@dataclass( frozen=True )
class AmenityOpeningScheduleProvider( Generic[ TOpeningSchedule, TScheduleRecord, TScheduleOverride ] ):
   name_field: AmenityNameField
   opening_table: str
   override_table: str
   map_records: Callable[ [ list[ Types.Row ] ], list[ TScheduleRecord ] ]

   @property
   def owner_column( self ) -> str:
      return self.name_field.value.upper()


   def _owner_name( self, row: Any ) -> str:
      return getattr( row, self.name_field.value )


   def overlaps_existing_schedule(
         self,
         conn: Types.Connection,
         schedule: TOpeningSchedule ) -> bool:
      cur = conn.cursor()

      try:
         row = cur.execute(
            f"""   SELECT 1
                  FROM { self.opening_table }
                  WHERE { self.owner_column } = ?
                     AND SCHEDULE_START_DATE != ?
                     AND SCHEDULE_START_DATE <= COALESCE( ?, ? )
                     AND COALESCE( SCHEDULE_END_DATE, ? ) >= ?
                  LIMIT 1;
            """,
            (
               self._owner_name( schedule ),
               schedule.start_date,
               schedule.end_date,
               Constants.OPEN_ENDED_SQL_DATE,
               Constants.OPEN_ENDED_SQL_DATE,
               schedule.start_date,
            ) ).fetchone()

         return row != None

      finally:
         cur.close()


   def fetch_opening_schedule_conflicts(
         self,
         conn: Types.Connection,
         schedule: TOpeningSchedule ) -> list[ TScheduleRecord ]:
      cur = conn.cursor()

      try:
         data = cur.execute(
            f"""   SELECT
                     { self.owner_column },
                     SCHEDULE_START_DATE,
                     SCHEDULE_END_DATE,
                     MONDAY,
                     TUESDAY,
                     WEDNESDAY,
                     THURSDAY,
                     FRIDAY,
                     SATURDAY,
                     SUNDAY,
                     HOLIDAYS_ONLY,
                     SCHEDULE_MESSAGE
                  FROM { self.opening_table }
                  WHERE { self.owner_column } = ?
                     AND SCHEDULE_START_DATE != ?
                     AND SCHEDULE_START_DATE <= COALESCE( ?, ? )
                     AND COALESCE( SCHEDULE_END_DATE, ? ) >= ?;
            """,
            (
               self._owner_name( schedule ),
               schedule.start_date,
               schedule.end_date,
               Constants.OPEN_ENDED_SQL_DATE,
               Constants.OPEN_ENDED_SQL_DATE,
               schedule.start_date,
            ) )

         return self.map_records( data.fetchall() )

      finally:
         cur.close()


   def delete_opening_schedule(
         self,
         conn: Types.Connection,
         schedule: TScheduleRecord ) -> None:
      cur = conn.cursor()

      try:
         cur.execute(
            f"""   DELETE FROM { self.opening_table }
                  WHERE { self.owner_column } = ?
                     AND SCHEDULE_START_DATE = ?;
            """,
            (
               self._owner_name( schedule ),
               schedule.schedule_start_date,
            ) )

      finally:
         cur.close()


   def update_opening_schedule_dates(
         self,
         conn: Types.Connection,
         schedule: TScheduleRecord,
         start_date: Types.DateKey,
         end_date: Types.DateKey | None ) -> None:
      cur = conn.cursor()

      try:
         cur.execute(
            f"""   UPDATE { self.opening_table }
                  SET
                     SCHEDULE_START_DATE = ?,
                     SCHEDULE_END_DATE = ?
                  WHERE { self.owner_column } = ?
                     AND SCHEDULE_START_DATE = ?;
            """,
            (
               start_date,
               end_date,
               self._owner_name( schedule ),
               schedule.schedule_start_date,
            ) )

      finally:
         cur.close()


   def insert_copied_opening_schedule(
         self,
         conn: Types.Connection,
         schedule: TScheduleRecord,
         start_date: Types.DateKey,
         end_date: Types.DateKey | None ) -> None:
      cur = conn.cursor()

      try:
         cur.execute(
            f"""   INSERT INTO { self.opening_table } (
                     { self.owner_column },
                     SCHEDULE_START_DATE,
                     SCHEDULE_END_DATE,
                     MONDAY,
                     TUESDAY,
                     WEDNESDAY,
                     THURSDAY,
                     FRIDAY,
                     SATURDAY,
                     SUNDAY,
                     HOLIDAYS_ONLY,
                     SCHEDULE_MESSAGE
                  )
                  VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);
            """,
            (
               self._owner_name( schedule ),
               start_date,
               end_date,
               schedule.monday,
               schedule.tuesday,
               schedule.wednesday,
               schedule.thursday,
               schedule.friday,
               schedule.saturday,
               schedule.sunday,
               schedule.holidays_only,
               schedule.schedule_message,
            ) )

      finally:
         cur.close()


   def insert_or_update_opening_schedule(
         self,
         conn: Types.Connection,
         schedule: TOpeningSchedule ) -> None:
      cur = conn.cursor()

      try:
         cur.execute(
            f"""   INSERT INTO { self.opening_table } (
                     { self.owner_column },
                     SCHEDULE_START_DATE,
                     SCHEDULE_END_DATE,
                     MONDAY,
                     TUESDAY,
                     WEDNESDAY,
                     THURSDAY,
                     FRIDAY,
                     SATURDAY,
                     SUNDAY,
                     HOLIDAYS_ONLY,
                     SCHEDULE_MESSAGE
                  )
                  VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                  ON CONFLICT({ self.owner_column }, SCHEDULE_START_DATE) DO UPDATE SET
                     SCHEDULE_END_DATE = excluded.SCHEDULE_END_DATE,
                     MONDAY = excluded.MONDAY,
                     TUESDAY = excluded.TUESDAY,
                     WEDNESDAY = excluded.WEDNESDAY,
                     THURSDAY = excluded.THURSDAY,
                     FRIDAY = excluded.FRIDAY,
                     SATURDAY = excluded.SATURDAY,
                     SUNDAY = excluded.SUNDAY,
                     HOLIDAYS_ONLY = excluded.HOLIDAYS_ONLY,
                     SCHEDULE_MESSAGE = excluded.SCHEDULE_MESSAGE;
            """,
            (
               self._owner_name( schedule ),
               schedule.start_date,
               schedule.end_date,
               schedule.monday,
               schedule.tuesday,
               schedule.wednesday,
               schedule.thursday,
               schedule.friday,
               schedule.saturday,
               schedule.sunday,
               schedule.holidays_only,
               schedule.message,
            ) )

      finally:
         cur.close()


   def save_schedule_override(
         self,
         conn: Types.Connection,
         override: TScheduleOverride ) -> bool:
      cur = conn.cursor()

      try:
         cur.execute(
            f"""   INSERT INTO { self.override_table } (
                     { self.owner_column },
                     OVERRIDE_START_DATE,
                     OVERRIDE_END_DATE,
                     IS_CLOSED,
                     OVERRIDE_MESSAGE
                  )
                  VALUES (?, ?, ?, ?, ?)
                  ON CONFLICT({ self.owner_column }, OVERRIDE_START_DATE) DO UPDATE SET
                     OVERRIDE_END_DATE = excluded.OVERRIDE_END_DATE,
                     IS_CLOSED = excluded.IS_CLOSED,
                     OVERRIDE_MESSAGE = excluded.OVERRIDE_MESSAGE;
            """,
            (
               self._owner_name( override ),
               override.start_date,
               override.end_date,
               override.is_closed,
               override.message,
            ) )

         conn.commit()
         return cur.rowcount > 0

      finally:
         cur.close()
