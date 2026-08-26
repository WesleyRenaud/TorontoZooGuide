from __future__ import annotations

from .emergency_intercom_mapper import EmergencyIntercomMapper
from ...models import EmergencyIntercom
from ...types import Connection


class EmergencyIntercomProvider():
   @classmethod
   def fetch_emergency_intercoms( cls, conn: Connection ) -> list[ EmergencyIntercom ]:
      cur = conn.cursor()

      try:
         data = cur.execute(
            """   SELECT
                     X_COORD,
                     Y_COORD
                  FROM EmergencyIntercom;
            """ )

         return EmergencyIntercomMapper.map_records( data.fetchall() )

      finally:
         cur.close()
