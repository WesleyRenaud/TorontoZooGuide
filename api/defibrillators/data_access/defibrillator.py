from __future__ import annotations

from .defibrillator_mapper import map_defibrillator_records
from ...models import Defibrillator
from ...types import Connection


def fetch_defibrillators( conn: Connection ) -> list[ Defibrillator ]:
   cur = conn.cursor()

   try:
      data = cur.execute(
         """   SELECT
                  X_COORD,
                  Y_COORD
               FROM Defibrillator;
         """ )

      return map_defibrillator_records( data.fetchall() )

   finally:
      cur.close()
