from __future__ import annotations

from .attraction_mapper import map_attraction_record
from .attraction_mapper import map_attraction_records
from .attraction_mapper import map_attraction_schedule_override_records
from .attraction_mapper import map_attraction_schedule_records
from .attraction_record import AttractionRecord
from .attraction_schedule_override_record import AttractionScheduleOverrideRecord
from .attraction_schedule_record import AttractionScheduleRecord
from ...types import Connection, VisitDay, VisitMonth


def fetch_attraction_names( conn: Connection ) -> list[ str ]:
   cur = conn.cursor()

   try:
      data = cur.execute(
         """   SELECT
                  a.NAME
               FROM Attraction a;
         """ )

      return [ row[ 0 ] for row in data.fetchall() ]

   finally:
      cur.close()


def fetch_attraction_records(
      conn: Connection,
      month: VisitMonth,
      day: VisitDay ) -> list[ AttractionRecord ]:
   cur = conn.cursor()

   try:
      data = cur.execute(
         """   SELECT
                  a.NAME,
                  a.FREE_WITH_ADMISSION,
                  a.DESCRIPTION,
                  a.INFO_LINK,
                  a.HYPERLINK_TEXT,
                  a.X_COORD,
                  a.Y_COORD,
                  COALESCE( adsam.WEEKDAY_VALUE, 1.0 ) AS ATTRACTION_DAY_SEASONAL_WEEKDAY_MULTIPLIER,
                  COALESCE( adsam.WEEKEND_HOLIDAY_VALUE, 1.0 ) AS ATTRACTION_DAY_SEASONAL_WEEKEND_HOLIDAY_MULTIPLIER
               FROM Attraction a
               LEFT JOIN AttractionDaySeasonalAvailabilityMultiplier adsam
                  ON a.NAME = adsam.ATTRACTION
                  AND adsam.MONTH = ?
                  AND adsam.DAY = ?;
         """, ( month, day ) )

      return map_attraction_records( data.fetchall() )

   finally:
      cur.close()


def fetch_attraction_record_for_calendar_day(
      conn: Connection,
      attraction_name: str,
      month: VisitMonth,
      day: VisitDay ) -> AttractionRecord | None:

   cur = conn.cursor()

   try:
      row = cur.execute(
         """   SELECT
                  a.NAME,
                  a.FREE_WITH_ADMISSION,
                  a.DESCRIPTION,
                  a.INFO_LINK,
                  a.HYPERLINK_TEXT,
                  a.X_COORD,
                  a.Y_COORD,
                  COALESCE( adsam.WEEKDAY_VALUE, 1.0 ) AS ATTRACTION_DAY_SEASONAL_WEEKDAY_MULTIPLIER,
                  COALESCE( adsam.WEEKEND_HOLIDAY_VALUE, 1.0 ) AS ATTRACTION_DAY_SEASONAL_WEEKEND_HOLIDAY_MULTIPLIER
               FROM Attraction a
               LEFT JOIN AttractionDaySeasonalAvailabilityMultiplier adsam
                  ON a.NAME = adsam.ATTRACTION
                  AND adsam.MONTH = ?
                  AND adsam.DAY = ?
               WHERE a.NAME = ?;
         """,
         ( month, day, attraction_name )
      ).fetchone()

      return map_attraction_record( row ) if row != None else None

   finally:
      cur.close()


def fetch_attraction_schedule_records( conn: Connection ) -> list[ AttractionScheduleRecord ]:
   cur = conn.cursor()

   try:
      data = cur.execute(
         """   SELECT
                  s.ATTRACTION,
                  s.SCHEDULE_START_DATE,
                  s.SCHEDULE_END_DATE,
                  s.MONDAY,
                  s.TUESDAY,
                  s.WEDNESDAY,
                  s.THURSDAY,
                  s.FRIDAY,
                  s.SATURDAY,
                  s.SUNDAY,
                  s.HOLIDAYS_ONLY,
                  s.SCHEDULE_MESSAGE
               FROM AttractionOpeningSchedule s;
         """ )

      return map_attraction_schedule_records( data.fetchall() )

   finally:
      cur.close()


def fetch_attraction_schedule_override_records(
      conn: Connection ) -> list[ AttractionScheduleOverrideRecord ]:
   cur = conn.cursor()

   try:
      data = cur.execute(
         """   SELECT
                  o.ATTRACTION,
                  o.OVERRIDE_START_DATE,
                  o.OVERRIDE_END_DATE,
                  o.IS_CLOSED,
                  o.OVERRIDE_MESSAGE
               FROM AttractionScheduleOverride o;
         """ )

      return map_attraction_schedule_override_records( data.fetchall() )

   finally:
      cur.close()
