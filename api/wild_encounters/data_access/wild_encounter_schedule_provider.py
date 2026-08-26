from __future__ import annotations

from ..scheduling.wild_encounter_schedule_end_input import WildEncounterScheduleEndInput
from ..scheduling.wild_encounter_schedule_input import WildEncounterScheduleInput
from ...shared.constants import OPEN_ENDED_SQL_DATE
from ...types import Connection, DateKey
from .wild_encounter_schedule_conflict_mapper import WildEncounterScheduleConflictMapper
from .wild_encounter_schedule_conflict_record import WildEncounterScheduleConflictRecord
from .wild_encounter_schedule_mapper import WildEncounterScheduleMapper
from .wild_encounter_schedule_record import WildEncounterScheduleRecord


class WildEncounterScheduleProvider():
   @classmethod
   def fetch_schedule_records(
         cls,
         conn: Connection,
         target_date: DateKey ) -> list[ WildEncounterScheduleRecord ]:
      cur = conn.cursor()

      try:
         data = cur.execute(
            """   -- VISIT_DATE
                  SELECT
                     w.NAME,
                     w.MEETING_SPOT,
                     w.LINK,
                     w.MAXIMUM_DURATION,
                     m.X_COORD,
                     m.Y_COORD,
                     m.REGION,
                     s.SCHEDULE_START_DATE,
                     s.SCHEDULE_END_DATE,
                     s.MONDAY,
                     s.TUESDAY,
                     s.WEDNESDAY,
                     s.THURSDAY,
                     s.FRIDAY,
                     s.SATURDAY,
                     s.SUNDAY,
                     s.ENCOUNTER_TIME,
                     c.WILD_ENCOUNTER IS NOT NULL AS IS_CANCELLED
                  FROM WildEncounter w
                  JOIN WildEncounterMeetingSpot m
                     ON w.MEETING_SPOT = m.NAME
                  JOIN WildEncounterSchedule s
                     ON w.NAME = s.WILD_ENCOUNTER
                  LEFT JOIN WildEncounterCancellation c
                     ON c.WILD_ENCOUNTER = s.WILD_ENCOUNTER
                     AND c.CANCELLATION_DATE = :VISIT_DATE
                     AND c.ENCOUNTER_TIME = s.ENCOUNTER_TIME
                  WHERE s.SCHEDULE_START_DATE <= :VISIT_DATE
                     AND (
                        s.SCHEDULE_END_DATE IS NULL
                        OR s.SCHEDULE_END_DATE >= :VISIT_DATE
                     );
            """,
            { 'VISIT_DATE': target_date } )

         return WildEncounterScheduleMapper.map_records( data.fetchall() )

      finally:
         cur.close()


   @classmethod
   def fetch_schedule_records_for_occurrences(
         cls,
         conn: Connection,
         wild_encounter: str ) -> list[ WildEncounterScheduleRecord ]:
      cur = conn.cursor()

      try:
         data = cur.execute(
            """   SELECT
                     w.NAME,
                     w.MEETING_SPOT,
                     w.LINK,
                     w.MAXIMUM_DURATION,
                     m.X_COORD,
                     m.Y_COORD,
                     m.REGION,
                     s.SCHEDULE_START_DATE,
                     s.SCHEDULE_END_DATE,
                     s.MONDAY,
                     s.TUESDAY,
                     s.WEDNESDAY,
                     s.THURSDAY,
                     s.FRIDAY,
                     s.SATURDAY,
                     s.SUNDAY,
                     s.ENCOUNTER_TIME,
                     0 AS IS_CANCELLED
                  FROM WildEncounter w
                  JOIN WildEncounterMeetingSpot m
                     ON w.MEETING_SPOT = m.NAME
                  JOIN WildEncounterSchedule s
                     ON w.NAME = s.WILD_ENCOUNTER
                  WHERE s.WILD_ENCOUNTER = ?
                  ORDER BY s.ENCOUNTER_TIME;
            """,
            ( wild_encounter, ) )

         return WildEncounterScheduleMapper.map_records( data.fetchall() )

      finally:
         cur.close()


   @classmethod
   def fetch_schedule_times(
         cls,
         conn: Connection,
         wild_encounter: str,
         target_date: DateKey ) -> list[ str ]:
      cur = conn.cursor()

      try:
         rows = cur.execute(
            """   SELECT DISTINCT ENCOUNTER_TIME
                  FROM WildEncounterSchedule
                  WHERE WILD_ENCOUNTER = ?
                     AND SCHEDULE_START_DATE <= ?
                     AND COALESCE( SCHEDULE_END_DATE, ? ) >= ?
                  ORDER BY ENCOUNTER_TIME;""",
            (
               wild_encounter,
               target_date,
               OPEN_ENDED_SQL_DATE,
               target_date,
            ) ).fetchall()

         return [ row[ 0 ] for row in rows ]

      finally:
         cur.close()


   @classmethod
   def schedule_overlaps_existing_schedule(
         cls,
         conn: Connection,
         schedule: WildEncounterScheduleInput ) -> bool:
      cur = conn.cursor()

      try:
         row = cur.execute(
            """   SELECT 1
                  FROM WildEncounterSchedule
                  WHERE WILD_ENCOUNTER = ?
                     AND ENCOUNTER_TIME = ?
                     AND SCHEDULE_START_DATE != ?
                     AND SCHEDULE_START_DATE <= COALESCE( ?, ? )
                     AND COALESCE( SCHEDULE_END_DATE, ? ) >= ?
                  LIMIT 1;
            """,
            (
               schedule.wild_encounter,
               schedule.encounter_time,
               schedule.start_date,
               schedule.end_date,
               OPEN_ENDED_SQL_DATE,
               OPEN_ENDED_SQL_DATE,
               schedule.start_date,
            ) ).fetchone()

         return row != None

      finally:
         cur.close()


   @classmethod
   def fetch_schedule_conflicts(
         cls,
         conn: Connection,
         schedule: WildEncounterScheduleInput ) -> list[ WildEncounterScheduleConflictRecord ]:
      cur = conn.cursor()

      try:
         data = cur.execute(
            """   SELECT
                     WILD_ENCOUNTER,
                     ENCOUNTER_TIME,
                     SCHEDULE_START_DATE,
                     SCHEDULE_END_DATE,
                     MONDAY,
                     TUESDAY,
                     WEDNESDAY,
                     THURSDAY,
                     FRIDAY,
                     SATURDAY,
                     SUNDAY,
                     SCHEDULE_MESSAGE
                  FROM WildEncounterSchedule
                  WHERE WILD_ENCOUNTER = ?
                     AND ENCOUNTER_TIME = ?
                     AND SCHEDULE_START_DATE != ?
                     AND SCHEDULE_START_DATE <= COALESCE( ?, ? )
                     AND COALESCE( SCHEDULE_END_DATE, ? ) >= ?;
            """,
            (
               schedule.wild_encounter,
               schedule.encounter_time,
               schedule.start_date,
               schedule.end_date,
               OPEN_ENDED_SQL_DATE,
               OPEN_ENDED_SQL_DATE,
               schedule.start_date,
            ) )

         return WildEncounterScheduleConflictMapper.map_records( data.fetchall() )

      finally:
         cur.close()


   @classmethod
   def delete_schedule(
         cls,
         conn: Connection,
         schedule: WildEncounterScheduleConflictRecord ) -> None:
      cur = conn.cursor()

      try:
         cur.execute(
            """   DELETE FROM WildEncounterSchedule
                  WHERE WILD_ENCOUNTER = ?
                     AND ENCOUNTER_TIME = ?
                     AND SCHEDULE_START_DATE = ?;
            """,
            (
               schedule.wild_encounter,
               schedule.encounter_time,
               schedule.schedule_start_date,
            ) )

      finally:
         cur.close()


   @classmethod
   def update_schedule_dates(
         cls,
         conn: Connection,
         schedule: WildEncounterScheduleConflictRecord,
         start_date: DateKey,
         end_date: DateKey | None ) -> None:
      cur = conn.cursor()

      try:
         cur.execute(
            """   UPDATE WildEncounterSchedule
                  SET
                     SCHEDULE_START_DATE = ?,
                     SCHEDULE_END_DATE = ?
                  WHERE WILD_ENCOUNTER = ?
                     AND ENCOUNTER_TIME = ?
                     AND SCHEDULE_START_DATE = ?;
            """,
            (
               start_date,
               end_date,
               schedule.wild_encounter,
               schedule.encounter_time,
               schedule.schedule_start_date,
            ) )

      finally:
         cur.close()


   @classmethod
   def insert_copied_schedule(
         cls,
         conn: Connection,
         schedule: WildEncounterScheduleConflictRecord,
         start_date: DateKey,
         end_date: DateKey | None ) -> None:
      cur = conn.cursor()

      try:
         cur.execute(
            """   INSERT INTO WildEncounterSchedule (
                     WILD_ENCOUNTER,
                     SCHEDULE_START_DATE,
                     SCHEDULE_END_DATE,
                     ENCOUNTER_TIME,
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
                     WILD_ENCOUNTER,
                     ?,
                     ?,
                     ENCOUNTER_TIME,
                     MONDAY,
                     TUESDAY,
                     WEDNESDAY,
                     THURSDAY,
                     FRIDAY,
                     SATURDAY,
                     SUNDAY,
                     SCHEDULE_MESSAGE
                  FROM WildEncounterSchedule
                  WHERE WILD_ENCOUNTER = ?
                     AND ENCOUNTER_TIME = ?
                     AND SCHEDULE_START_DATE = ?;
            """,
            (
               start_date,
               end_date,
               schedule.wild_encounter,
               schedule.encounter_time,
               schedule.schedule_start_date,
            ) )

      finally:
         cur.close()


   @classmethod
   def insert_or_update_schedule(
         cls,
         conn: Connection,
         schedule: WildEncounterScheduleInput ) -> None:
      cur = conn.cursor()

      try:
         cur.execute(
            """   INSERT INTO WildEncounterSchedule (
                     WILD_ENCOUNTER,
                     SCHEDULE_START_DATE,
                     SCHEDULE_END_DATE,
                     ENCOUNTER_TIME,
                     MONDAY,
                     TUESDAY,
                     WEDNESDAY,
                     THURSDAY,
                     FRIDAY,
                     SATURDAY,
                     SUNDAY,
                     SCHEDULE_MESSAGE
                  )
                  VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                  ON CONFLICT(WILD_ENCOUNTER, ENCOUNTER_TIME, SCHEDULE_START_DATE) DO UPDATE SET
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
               schedule.wild_encounter,
               schedule.start_date,
               schedule.end_date,
               schedule.encounter_time,
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
         conn: Connection,
         schedule: WildEncounterScheduleInput ) -> bool:
      if cls.schedule_overlaps_existing_schedule( conn, schedule ):
         return False

      cls.insert_or_update_schedule( conn, schedule )
      conn.commit()
      return True


   @classmethod
   def save_schedule_end(
         cls,
         conn: Connection,
         schedule_end: WildEncounterScheduleEndInput ) -> bool:
      cur = conn.cursor()

      try:
         cur.execute(
            """   UPDATE WildEncounterSchedule
                  SET SCHEDULE_END_DATE = ?
                  WHERE WILD_ENCOUNTER = ?
                     AND ENCOUNTER_TIME = ?
                     AND SCHEDULE_START_DATE <= ?
                     AND COALESCE( SCHEDULE_END_DATE, ? ) >= ?;
            """,
            (
               schedule_end.schedule_end_date,
               schedule_end.wild_encounter,
               schedule_end.encounter_time,
               schedule_end.schedule_end_date,
               OPEN_ENDED_SQL_DATE,
               schedule_end.schedule_end_date,
            ) )

         conn.commit()
         return cur.rowcount > 0

      finally:
         cur.close()
