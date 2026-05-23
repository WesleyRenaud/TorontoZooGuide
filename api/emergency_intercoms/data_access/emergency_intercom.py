from __future__ import annotations

from ... import zoo
from ...types import Connection
from .emergency_intercom_mapper import map_emergency_intercom_records


def fetch_emergency_intercoms( conn: Connection ) -> list[ zoo.EmergencyIntercom ]:
   cur = conn.cursor()

   try:
      data = cur.execute(
         """   SELECT
                  X_COORD,
                  Y_COORD
               FROM EmergencyIntercom;
         """ )

      return map_emergency_intercom_records( data.fetchall() )

   finally:
      cur.close()
