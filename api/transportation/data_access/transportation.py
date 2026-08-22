from __future__ import annotations

from datetime import date

from ...shared.constants import OPEN_ENDED_SQL_DATE
from .transportation_mapper import map_transportation_records
from .transportation_record import TransportationRecord
from ...types import Connection


def fetch_transportation_records(
      conn: Connection,
      visit_date: date ) -> list[ TransportationRecord ]:
   cur = conn.cursor()

   try:
      rows = cur.execute(
         """   SELECT
                  t.NAME,
                  t.IS_ALSO_ATTRACTION,
                  a.FREE_WITH_ADMISSION,
                  a.DESCRIPTION,
                  a.INFO_LINK,
                  a.HYPERLINK_TEXT,
                  a.X_COORD,
                  a.Y_COORD,
                  a.REGION,
                  ahs.WEEKDAY_START_TIME,
                  ahs.WEEKDAY_END_TIME,
                  ahs.WEEKEND_HOLIDAY_START_TIME,
                  ahs.WEEKEND_HOLIDAY_END_TIME
               FROM Transportation t
               JOIN Attraction a
                 ON a.NAME = t.NAME
               LEFT JOIN AttractionHoursSchedule ahs
                  ON a.NAME = ahs.ATTRACTION
                  AND ahs.SCHEDULE_START_DATE <= ?
                  AND COALESCE( ahs.SCHEDULE_END_DATE, ? ) >= ?
               ORDER BY t.NAME;
         """,
         (
            visit_date,
            OPEN_ENDED_SQL_DATE,
            visit_date,
         )
      ).fetchall()

      return map_transportation_records( rows )

   finally:
      cur.close()
