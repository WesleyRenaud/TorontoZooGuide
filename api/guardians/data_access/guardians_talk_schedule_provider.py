from __future__ import annotations

from .guardians_talk_schedule_mapper import GuardiansTalkScheduleMapper
from .guardians_talk_schedule_record import GuardiansTalkScheduleRecord
from ..scheduling.guardians_talk_schedule_end_input import GuardiansTalkScheduleEndInput
from ..scheduling.guardians_talk_schedule_input import GuardiansTalkScheduleInput
from ...shared.constants import Constants
from ...shared.enums.position import Position
from ...types import Types


class GuardiansTalkScheduleProvider():
   @classmethod
   def fetch_schedule_records( cls, conn: Types.Connection ) -> list[ GuardiansTalkScheduleRecord ]:
      cur = conn.cursor()

      try:
         data = cur.execute(
            """   SELECT
                     t.NAME,
                     t.LOCATION,
                     t.ENCLOSURE_NAME,
                     t.X_COORD,
                     t.Y_COORD,
                     t.MAXIMUM_DURATION,
                     s.SCHEDULE_START_DATE,
                     s.SCHEDULE_END_DATE,
                     s.MONDAY,
                     s.TUESDAY,
                     s.WEDNESDAY,
                     s.THURSDAY,
                     s.FRIDAY,
                     s.SATURDAY,
                     s.SUNDAY,
                     s.TALK_TIME
                  FROM MeetTheGuardiansTalk t
                  JOIN GuardiansTalkSchedule s
                     ON t.NAME = s.TALK_NAME
                     AND t.LOCATION = s.LOCATION
                     AND t.ENCLOSURE_NAME IS s.ENCLOSURE_NAME;
            """ )

         return GuardiansTalkScheduleMapper.map_records( data.fetchall() )

      finally:
         cur.close()


   @classmethod
   def fetch_schedule_records_for_talk(
         cls,
         conn: Types.Connection,
         talk_name: str,
         location: str,
         *,
         enclosure_name: str ) -> list[ GuardiansTalkScheduleRecord ]:
      cur = conn.cursor()

      try:
         data = cur.execute(
            """   SELECT
                     t.NAME,
                     t.LOCATION,
                     t.ENCLOSURE_NAME,
                     t.X_COORD,
                     t.Y_COORD,
                     t.MAXIMUM_DURATION,
                     s.SCHEDULE_START_DATE,
                     s.SCHEDULE_END_DATE,
                     s.MONDAY,
                     s.TUESDAY,
                     s.WEDNESDAY,
                     s.THURSDAY,
                     s.FRIDAY,
                     s.SATURDAY,
                     s.SUNDAY,
                     s.TALK_TIME
                  FROM MeetTheGuardiansTalk t
                  JOIN GuardiansTalkSchedule s
                     ON t.NAME = s.TALK_NAME
                     AND t.LOCATION = s.LOCATION
                     AND t.ENCLOSURE_NAME IS s.ENCLOSURE_NAME
                  WHERE s.TALK_NAME = ?
                  AND s.LOCATION = ?
                  AND s.ENCLOSURE_NAME IS ?
                  ORDER BY s.TALK_TIME, s.SCHEDULE_START_DATE;
            """,
            (
               talk_name,
               location,
               enclosure_name,
            ) )

         return GuardiansTalkScheduleMapper.map_records( data.fetchall() )

      finally:
         cur.close()


   @classmethod
   def fetch_schedule_records_for_occurrences(
         cls,
         conn: Types.Connection,
         talk_name: str,
         location: str,
         *,
         enclosure_name: str ) -> list[ GuardiansTalkScheduleRecord ]:
      return cls.fetch_schedule_records_for_talk(
         conn,
         talk_name=talk_name,
         location=location,
         enclosure_name=enclosure_name )


   @classmethod
   def fetch_schedule_records_covering_date(
         cls,
         conn: Types.Connection,
         *,
         talk_name: str,
         location: str,
         talk_time: str,
         occurrence_date: Types.DateKey,
         enclosure_name: str ) -> list[ GuardiansTalkScheduleRecord ]:
      cur = conn.cursor()

      try:
         data = cur.execute(
            """   SELECT
                     t.NAME,
                     t.LOCATION,
                     t.ENCLOSURE_NAME,
                     t.X_COORD,
                     t.Y_COORD,
                     t.MAXIMUM_DURATION,
                     s.SCHEDULE_START_DATE,
                     s.SCHEDULE_END_DATE,
                     s.MONDAY,
                     s.TUESDAY,
                     s.WEDNESDAY,
                     s.THURSDAY,
                     s.FRIDAY,
                     s.SATURDAY,
                     s.SUNDAY,
                     s.TALK_TIME
                  FROM MeetTheGuardiansTalk t
                  JOIN GuardiansTalkSchedule s
                     ON t.NAME = s.TALK_NAME
                     AND t.LOCATION = s.LOCATION
                     AND t.ENCLOSURE_NAME IS s.ENCLOSURE_NAME
                  WHERE s.TALK_NAME = ?
                     AND s.LOCATION = ?
                     AND s.ENCLOSURE_NAME IS ?
                     AND s.TALK_TIME = ?
                     AND s.SCHEDULE_START_DATE <= ?
                     AND COALESCE( s.SCHEDULE_END_DATE, ? ) > ?;
            """,
            (
               talk_name,
               location,
               enclosure_name,
               talk_time,
               occurrence_date,
               Constants.OPEN_ENDED_SQL_DATE,
               occurrence_date,
            ) )

         return GuardiansTalkScheduleMapper.map_records( data.fetchall() )

      finally:
         cur.close()


   @classmethod
   def fetch_day_schedule_records_from_schedule(
         cls,
         conn: Types.Connection,
         target_date: Types.DateKey ) -> list[ GuardiansTalkScheduleRecord ]:
      cur = conn.cursor()

      try:
         data = cur.execute(
            """   SELECT
                     t.NAME,
                     t.LOCATION,
                     t.ENCLOSURE_NAME,
                     t.X_COORD,
                     t.Y_COORD,
                     t.MAXIMUM_DURATION,
                     s.SCHEDULE_START_DATE,
                     s.SCHEDULE_END_DATE,
                     s.MONDAY,
                     s.TUESDAY,
                     s.WEDNESDAY,
                     s.THURSDAY,
                     s.FRIDAY,
                     s.SATURDAY,
                     s.SUNDAY,
                     s.TALK_TIME
                  FROM MeetTheGuardiansTalk t
                  JOIN GuardiansTalkSchedule s
                     ON t.NAME = s.TALK_NAME
                     AND t.LOCATION = s.LOCATION
                     AND t.ENCLOSURE_NAME IS s.ENCLOSURE_NAME
                  WHERE s.SCHEDULE_START_DATE <= ?
                     AND COALESCE( s.SCHEDULE_END_DATE, ? ) > ?
                     AND NOT EXISTS (
                        SELECT 1
                        FROM GuardiansTalkCancellation c
                        WHERE c.TALK_NAME = s.TALK_NAME
                           AND c.LOCATION = s.LOCATION
                           AND c.ENCLOSURE_NAME IS s.ENCLOSURE_NAME
                           AND c.CANCELLATION_DATE = ?
                           AND c.TALK_TIME = s.TALK_TIME
                     );
            """,
            (
               target_date,
               Constants.OPEN_ENDED_SQL_DATE,
               target_date,
               target_date,
            ) )

         return GuardiansTalkScheduleMapper.map_records( data.fetchall() )

      finally:
         cur.close()


   @classmethod
   def fetch_schedule_times(
         cls,
         conn: Types.Connection,
         talk_name: str,
         location: str,
         target_date: Types.DateKey,
         *,
         enclosure_name: str ) -> list[ str ]:
      cur = conn.cursor()

      try:
         rows = cur.execute(
            """   SELECT DISTINCT
                     TALK_TIME
                  FROM GuardiansTalkSchedule
                  WHERE TALK_NAME = ?
                     AND LOCATION = ?
                     AND ENCLOSURE_NAME IS ?
                     AND COALESCE( SCHEDULE_END_DATE, ? ) > ?
                  ORDER BY TALK_TIME;""",
            (
               talk_name,
               location,
               enclosure_name,
               Constants.OPEN_ENDED_SQL_DATE,
               target_date,
            ) ).fetchall()

         return [ row[ Position.FIRST ] for row in rows ]

      finally:
         cur.close()


   @classmethod
   def schedule_overlaps_existing_schedule(
         cls,
         conn: Types.Connection,
         schedule: GuardiansTalkScheduleInput ) -> bool:
      cur = conn.cursor()

      try:
         row = cur.execute(
            """   SELECT 1
                  FROM GuardiansTalkSchedule
                  WHERE TALK_NAME = ?
                     AND LOCATION = ?
                     AND ENCLOSURE_NAME IS ?
                     AND TALK_TIME = ?
                     AND SCHEDULE_START_DATE != ?
                     AND SCHEDULE_START_DATE <= COALESCE( ?, ? )
                     AND COALESCE( SCHEDULE_END_DATE, ? ) >= ?
                  LIMIT 1;
            """,
            (
               schedule.talk_name,
               schedule.location,
               schedule.enclosure_name,
               schedule.talk_time,
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
   def fetch_schedule_conflicts(
         cls,
         conn: Types.Connection,
         schedule: GuardiansTalkScheduleInput ) -> list[ GuardiansTalkScheduleRecord ]:
      cur = conn.cursor()

      try:
         data = cur.execute(
            """   SELECT
                     t.NAME,
                     t.LOCATION,
                     t.ENCLOSURE_NAME,
                     t.X_COORD,
                     t.Y_COORD,
                     t.MAXIMUM_DURATION,
                     s.SCHEDULE_START_DATE,
                     s.SCHEDULE_END_DATE,
                     s.MONDAY,
                     s.TUESDAY,
                     s.WEDNESDAY,
                     s.THURSDAY,
                     s.FRIDAY,
                     s.SATURDAY,
                     s.SUNDAY,
                     s.TALK_TIME
                  FROM MeetTheGuardiansTalk t
                  JOIN GuardiansTalkSchedule s
                     ON t.NAME = s.TALK_NAME
                     AND t.LOCATION = s.LOCATION
                     AND t.ENCLOSURE_NAME IS s.ENCLOSURE_NAME
                  WHERE s.TALK_NAME = ?
                     AND s.LOCATION = ?
                     AND s.ENCLOSURE_NAME IS ?
                     AND s.TALK_TIME = ?
                     AND s.SCHEDULE_START_DATE != ?
                     AND s.SCHEDULE_START_DATE <= COALESCE( ?, ? )
                     AND COALESCE( s.SCHEDULE_END_DATE, ? ) >= ?;
            """,
            (
               schedule.talk_name,
               schedule.location,
               schedule.enclosure_name,
               schedule.talk_time,
               schedule.start_date,
               schedule.end_date,
               Constants.OPEN_ENDED_SQL_DATE,
               Constants.OPEN_ENDED_SQL_DATE,
               schedule.start_date,
            ) )

         return GuardiansTalkScheduleMapper.map_records( data.fetchall() )

      finally:
         cur.close()


   @classmethod
   def delete_schedule(
         cls,
         conn: Types.Connection,
         schedule: GuardiansTalkScheduleRecord ) -> None:
      cur = conn.cursor()

      try:
         cur.execute(
            """   DELETE FROM GuardiansTalkSchedule
                  WHERE TALK_NAME = ?
                     AND LOCATION = ?
                     AND ENCLOSURE_NAME IS ?
                     AND TALK_TIME = ?
                     AND SCHEDULE_START_DATE = ?;
            """,
            (
               schedule.name,
               schedule.location,
               schedule.enclosure_name,
               schedule.talk_time,
               schedule.schedule_start_date,
            ) )

      finally:
         cur.close()


   @classmethod
   def update_schedule_dates(
         cls,
         conn: Types.Connection,
         schedule: GuardiansTalkScheduleRecord,
         start_date: Types.DateKey,
         end_date: Types.DateKey | None ) -> None:
      cur = conn.cursor()

      try:
         cur.execute(
            """   UPDATE GuardiansTalkSchedule
                  SET
                     SCHEDULE_START_DATE = ?,
                     SCHEDULE_END_DATE = ?
                  WHERE TALK_NAME = ?
                     AND LOCATION = ?
                     AND ENCLOSURE_NAME IS ?
                     AND TALK_TIME = ?
                     AND SCHEDULE_START_DATE = ?;
            """,
            (
               start_date,
               end_date,
               schedule.name,
               schedule.location,
               schedule.enclosure_name,
               schedule.talk_time,
               schedule.schedule_start_date,
            ) )

      finally:
         cur.close()


   @classmethod
   def insert_copied_schedule(
         cls,
         conn: Types.Connection,
         schedule: GuardiansTalkScheduleRecord,
         start_date: Types.DateKey,
         end_date: Types.DateKey | None ) -> None:
      cur = conn.cursor()

      try:
         cur.execute(
            """   INSERT INTO GuardiansTalkSchedule (
                     TALK_NAME,
                     LOCATION,
                     ENCLOSURE_NAME,
                     SCHEDULE_START_DATE,
                     SCHEDULE_END_DATE,
                     TALK_TIME,
                     MONDAY,
                     TUESDAY,
                     WEDNESDAY,
                     THURSDAY,
                     FRIDAY,
                     SATURDAY,
                     SUNDAY,
                     SCHEDULE_MESSAGE
                  )
                  SELECT
                     TALK_NAME,
                     LOCATION,
                     ENCLOSURE_NAME,
                     ?,
                     ?,
                     TALK_TIME,
                     MONDAY,
                     TUESDAY,
                     WEDNESDAY,
                     THURSDAY,
                     FRIDAY,
                     SATURDAY,
                     SUNDAY,
                     SCHEDULE_MESSAGE
                  FROM GuardiansTalkSchedule
                  WHERE TALK_NAME = ?
                     AND LOCATION = ?
                     AND ENCLOSURE_NAME IS ?
                     AND TALK_TIME = ?
                     AND SCHEDULE_START_DATE = ?;
            """,
            (
               start_date,
               end_date,
               schedule.name,
               schedule.location,
               schedule.enclosure_name,
               schedule.talk_time,
               schedule.schedule_start_date,
            ) )

      finally:
         cur.close()


   @classmethod
   def insert_or_update_schedule(
         cls,
         conn: Types.Connection,
         schedule: GuardiansTalkScheduleInput ) -> None:
      cur = conn.cursor()

      try:
         cur.execute(
            """   INSERT INTO GuardiansTalkSchedule (
                     TALK_NAME,
                     LOCATION,
                     ENCLOSURE_NAME,
                     SCHEDULE_START_DATE,
                     SCHEDULE_END_DATE,
                     TALK_TIME,
                     MONDAY,
                     TUESDAY,
                     WEDNESDAY,
                     THURSDAY,
                     FRIDAY,
                     SATURDAY,
                     SUNDAY,
                     SCHEDULE_MESSAGE
                  )
                  VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                  ON CONFLICT(TALK_NAME, LOCATION, ENCLOSURE_NAME, TALK_TIME, SCHEDULE_START_DATE) DO UPDATE SET
                     SCHEDULE_END_DATE = excluded.SCHEDULE_END_DATE,
                     MONDAY = excluded.MONDAY,
                     TUESDAY = excluded.TUESDAY,
                     WEDNESDAY = excluded.WEDNESDAY,
                     THURSDAY = excluded.THURSDAY,
                     FRIDAY = excluded.FRIDAY,
                     SATURDAY = excluded.SATURDAY,
                     SUNDAY = excluded.SUNDAY,
                     SCHEDULE_MESSAGE = excluded.SCHEDULE_MESSAGE;
            """,
            (
               schedule.talk_name,
               schedule.location,
               schedule.enclosure_name,
               schedule.start_date,
               schedule.end_date,
               schedule.talk_time,
               schedule.monday,
               schedule.tuesday,
               schedule.wednesday,
               schedule.thursday,
               schedule.friday,
               schedule.saturday,
               schedule.sunday,
               schedule.message,
            ) )

      finally:
         cur.close()


   @classmethod
   def save_schedule(
         cls,
         conn: Types.Connection,
         schedule: GuardiansTalkScheduleInput ) -> bool:
      if cls.schedule_overlaps_existing_schedule( conn, schedule ):
         return False

      cls.insert_or_update_schedule( conn, schedule )
      conn.commit()
      return True


   @classmethod
   def save_schedule_end(
         cls,
         conn: Types.Connection,
         schedule_end: GuardiansTalkScheduleEndInput ) -> bool:
      cur = conn.cursor()

      try:
         cur.execute(
            """   UPDATE GuardiansTalkSchedule
                  SET SCHEDULE_END_DATE = ?
                  WHERE TALK_NAME = ?
                  AND LOCATION = ?
                  AND ENCLOSURE_NAME IS ?
                  AND TALK_TIME = ?
                  AND COALESCE( SCHEDULE_END_DATE, ? ) >= ?;
            """,
            (
               schedule_end.schedule_end_date,
               schedule_end.talk_name,
               schedule_end.location,
               schedule_end.enclosure_name,
               schedule_end.talk_time,
               Constants.OPEN_ENDED_SQL_DATE,
               schedule_end.schedule_end_date,
            ) )

         conn.commit()
         return cur.rowcount > 0

      finally:
         cur.close()
