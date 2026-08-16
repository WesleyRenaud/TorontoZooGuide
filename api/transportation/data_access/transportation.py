from __future__ import annotations

from .transportation_mapper import map_transportation_records
from .transportation_record import TransportationRecord
from ...types import Connection


def fetch_transportation_records(
      conn: Connection ) -> list[ TransportationRecord ]:
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
                  a.REGION
               FROM Transportation t
               JOIN Attraction a
                 ON a.NAME = t.NAME
               ORDER BY t.NAME;
         """
      ).fetchall()

      return map_transportation_records( rows )

   finally:
      cur.close()
