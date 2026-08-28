from __future__ import annotations

from .attraction_hours_schedule_mapper import AttractionHoursScheduleMapper
from .attraction_hours_schedule_record import AttractionHoursScheduleRecord
from ..scheduling.attraction_hours_schedule import AttractionHoursSchedule
from ...shared.constants import Constants
from ...types import Types


class AttractionHoursScheduleProvider():
   @classmethod
   def overlaps_existing_schedule(
         cls,
         conn: Types.Connection,
         schedule: AttractionHoursSchedule ) -> bool:
      cur = conn.cursor()
      try:
         row = cur.execute(
            """   SELECT 1
                  FROM AttractionHoursSchedule
                  WHERE ATTRACTION = ?
                     AND SCHEDULE_START_DATE != ?
                     AND SCHEDULE_START_DATE <= COALESCE( ?, ? )
                     AND COALESCE( SCHEDULE_END_DATE, ? ) >= ?
                  LIMIT 1;
            """,
            (
               schedule.attraction,
               schedule.start_date,
               schedule.end_date,
               Constants.OPEN_ENDED_SQL_DATE,
               Constants.OPEN_ENDED_SQL_DATE,
               schedule.start_date,
            ) ).fetchone()
         return row != None
      finally:
         cur.close()


   @classmethod
   def save_hours_schedule(
         cls,
         conn: Types.Connection,
         schedule: AttractionHoursSchedule ) -> bool:
      if cls.overlaps_existing_schedule( conn, schedule ):
         return False
      cls.insert_or_update_hours_schedule( conn, schedule )
      conn.commit()
      return True


   @classmethod
   def fetch_hours_schedule_conflicts(
         cls,
         conn: Types.Connection,
         schedule: AttractionHoursSchedule ) -> list[ AttractionHoursScheduleRecord ]:
      cur = conn.cursor()
      try:
         data = cur.execute(
            """   SELECT
                     ATTRACTION,
                     SCHEDULE_START_DATE,
                     SCHEDULE_END_DATE,
                     WEEKDAY_START_TIME,
                     WEEKDAY_END_TIME,
                     WEEKEND_HOLIDAY_START_TIME,
                     WEEKEND_HOLIDAY_END_TIME
                  FROM AttractionHoursSchedule
                  WHERE ATTRACTION = ?
                     AND SCHEDULE_START_DATE != ?
                     AND SCHEDULE_START_DATE <= COALESCE( ?, ? )
                     AND COALESCE( SCHEDULE_END_DATE, ? ) >= ?;
            """,
            (
               schedule.attraction,
               schedule.start_date,
               schedule.end_date,
               Constants.OPEN_ENDED_SQL_DATE,
               Constants.OPEN_ENDED_SQL_DATE,
               schedule.start_date,
            ) )
         return AttractionHoursScheduleMapper.map_records( data.fetchall() )
      finally:
         cur.close()


   @classmethod
   def fetch_hours_schedule_records(
         cls,
         conn: Types.Connection ) -> list[ AttractionHoursScheduleRecord ]:
      cur = conn.cursor()
      try:
         data = cur.execute(
            """   SELECT
                     ATTRACTION,
                     SCHEDULE_START_DATE,
                     SCHEDULE_END_DATE,
                     WEEKDAY_START_TIME,
                     WEEKDAY_END_TIME,
                     WEEKEND_HOLIDAY_START_TIME,
                     WEEKEND_HOLIDAY_END_TIME
                  FROM AttractionHoursSchedule
                  ORDER BY ATTRACTION, SCHEDULE_START_DATE;
            """ )
         return AttractionHoursScheduleMapper.map_records( data.fetchall() )
      finally:
         cur.close()


   @classmethod
   def delete_hours_schedule(
         cls,
         conn: Types.Connection,
         schedule: AttractionHoursScheduleRecord ) -> None:
      cur = conn.cursor()
      try:
         cur.execute(
            """   DELETE FROM AttractionHoursSchedule
                  WHERE ATTRACTION = ?
                     AND SCHEDULE_START_DATE = ?;
            """,
            ( schedule.attraction, schedule.schedule_start_date ) )
      finally:
         cur.close()


   @classmethod
   def update_hours_schedule_dates(
         cls,
         conn: Types.Connection,
         schedule: AttractionHoursScheduleRecord,
         start_date: Types.DateKey,
         end_date: Types.DateKey | None ) -> None:
      cur = conn.cursor()
      try:
         cur.execute(
            """   UPDATE AttractionHoursSchedule
                  SET
                     SCHEDULE_START_DATE = ?,
                     SCHEDULE_END_DATE = ?
                  WHERE ATTRACTION = ?
                     AND SCHEDULE_START_DATE = ?;
            """,
            (
               start_date,
               end_date,
               schedule.attraction,
               schedule.schedule_start_date,
            ) )
      finally:
         cur.close()


   @classmethod
   def insert_copied_hours_schedule(
         cls,
         conn: Types.Connection,
         schedule: AttractionHoursScheduleRecord,
         start_date: Types.DateKey,
         end_date: Types.DateKey | None ) -> None:
      cur = conn.cursor()
      try:
         cur.execute(
            """   INSERT INTO AttractionHoursSchedule (
                     ATTRACTION,
                     SCHEDULE_START_DATE,
                     SCHEDULE_END_DATE,
                     WEEKDAY_START_TIME,
                     WEEKDAY_END_TIME,
                     WEEKEND_HOLIDAY_START_TIME,
                     WEEKEND_HOLIDAY_END_TIME
                  )
                  VALUES (?, ?, ?, ?, ?, ?, ?);
            """,
            (
               schedule.attraction,
               start_date,
               end_date,
               schedule.weekday_start_time,
               schedule.weekday_end_time,
               schedule.weekend_holiday_start_time,
               schedule.weekend_holiday_end_time,
            ) )
      finally:
         cur.close()


   @classmethod
   def insert_or_update_hours_schedule(
         cls,
         conn: Types.Connection,
         schedule: AttractionHoursSchedule ) -> None:
      cur = conn.cursor()
      try:
         cur.execute(
            """   INSERT INTO AttractionHoursSchedule (
                     ATTRACTION,
                     SCHEDULE_START_DATE,
                     SCHEDULE_END_DATE,
                     WEEKDAY_START_TIME,
                     WEEKDAY_END_TIME,
                     WEEKEND_HOLIDAY_START_TIME,
                     WEEKEND_HOLIDAY_END_TIME
                  )
                  VALUES (?, ?, ?, ?, ?, ?, ?)
                  ON CONFLICT(ATTRACTION, SCHEDULE_START_DATE) DO UPDATE SET
                     SCHEDULE_END_DATE = excluded.SCHEDULE_END_DATE,
                     WEEKDAY_START_TIME = excluded.WEEKDAY_START_TIME,
                     WEEKDAY_END_TIME = excluded.WEEKDAY_END_TIME,
                     WEEKEND_HOLIDAY_START_TIME = excluded.WEEKEND_HOLIDAY_START_TIME,
                     WEEKEND_HOLIDAY_END_TIME = excluded.WEEKEND_HOLIDAY_END_TIME;
            """,
            (
               schedule.attraction,
               schedule.start_date,
               schedule.end_date,
               schedule.weekday_start_time,
               schedule.weekday_end_time,
               schedule.weekend_holiday_start_time,
               schedule.weekend_holiday_end_time,
            ) )
      finally:
         cur.close()
