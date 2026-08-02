from __future__ import annotations

from typing import TYPE_CHECKING

from .guardians_talk_day_schedule_mapper import map_guardians_talk_day_schedule_records
from .guardians_talk_day_schedule_record import GuardiansTalkDayScheduleRecord
from .guardians_talk_occurrence_mapper import map_guardians_talk_occurrence_records
from .guardians_talk_occurrence_record import GuardiansTalkOccurrenceRecord
from ...types import Connection, DateKey

if TYPE_CHECKING:
   from ..occurrences.guardians_talk_occurrence_input import GuardiansTalkOccurrenceInput


def guardians_talk_occurrence_record_exists(
      conn: Connection,
      talk_name: str,
      location: str,
      occurrence_date: DateKey,
      talk_time: str ) -> bool:
   cur = conn.cursor()

   try:
      row = cur.execute(
         """   SELECT 1
               FROM GuardiansTalkOccurrence
               WHERE TALK_NAME = ?
                  AND LOCATION = ?
                  AND OCCURRENCE_DATE = ?
                  AND TALK_TIME = ?
               LIMIT 1;
         """,
         (
            talk_name,
            location,
            occurrence_date,
            talk_time,
         ) ).fetchone()

      return row is not None

   finally:
      cur.close()


def save_guardians_talk_occurrence(
      conn: Connection,
      occurrence: GuardiansTalkOccurrenceInput ) -> bool:
   cur = conn.cursor()

   try:
      cur.execute(
         """   INSERT INTO GuardiansTalkOccurrence (
                  TALK_NAME,
                  LOCATION,
                  OCCURRENCE_DATE,
                  TALK_TIME
               )
               VALUES (?, ?, ?, ?)
               ON CONFLICT(TALK_NAME, LOCATION, OCCURRENCE_DATE, TALK_TIME)
               DO NOTHING;
         """,
         (
            occurrence.talk_name,
            occurrence.location,
            occurrence.occurrence_date,
            occurrence.talk_time,
         ) )

      conn.commit()
      return cur.rowcount > 0

   finally:
      cur.close()


def fetch_guardians_talk_occurrence_records(
      conn: Connection,
      talk_name: str,
      location: str,
      *,
      start_date: DateKey,
      end_date: DateKey ) -> list[ GuardiansTalkOccurrenceRecord ]:
   cur = conn.cursor()

   try:
      data = cur.execute(
         """   SELECT
                  OCCURRENCE_DATE,
                  TALK_TIME
               FROM GuardiansTalkOccurrence
               WHERE TALK_NAME = ?
                  AND LOCATION = ?
                  AND OCCURRENCE_DATE >= ?
                  AND OCCURRENCE_DATE <= ?
               ORDER BY OCCURRENCE_DATE, TALK_TIME;
         """,
         (
            talk_name,
            location,
            start_date,
            end_date,
         ) )

      return map_guardians_talk_occurrence_records( data.fetchall() )

   finally:
      cur.close()


def fetch_guardians_talk_day_schedule_records_from_occurrences(
      conn: Connection,
      target_date: DateKey ) -> list[ GuardiansTalkDayScheduleRecord ]:
   cur = conn.cursor()

   try:
      data = cur.execute(
         """   SELECT
                  t.NAME,
                  t.LOCATION,
                  t.X_COORD,
                  t.Y_COORD,
                  t.MAXIMUM_DURATION,
                  o.TALK_TIME
               FROM MeetTheGuardiansTalk t
               JOIN GuardiansTalkOccurrence o
                  ON t.NAME = o.TALK_NAME
                  AND t.LOCATION = o.LOCATION
               WHERE o.OCCURRENCE_DATE = ?
                  AND NOT EXISTS (
                     SELECT 1
                     FROM GuardiansTalkCancellation c
                     WHERE c.TALK_NAME = o.TALK_NAME
                        AND c.LOCATION = o.LOCATION
                        AND c.CANCELLATION_DATE = o.OCCURRENCE_DATE
                        AND c.TALK_TIME = o.TALK_TIME
                  )
               ORDER BY o.TALK_TIME, t.NAME, t.LOCATION;
         """,
         ( target_date, ) )

      return map_guardians_talk_day_schedule_records( data.fetchall() )

   finally:
      cur.close()
