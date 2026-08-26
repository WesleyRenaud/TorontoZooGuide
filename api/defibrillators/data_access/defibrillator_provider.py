from __future__ import annotations

from .defibrillator_mapper import DefibrillatorMapper
from ...models import Defibrillator
from ...types import Connection


class DefibrillatorProvider():
   @classmethod
   def fetch_defibrillators( cls, conn: Connection ) -> list[ Defibrillator ]:
      cur = conn.cursor()

      try:
         data = cur.execute(
            """   SELECT
                     X_COORD,
                     Y_COORD
                  FROM Defibrillator;
            """ )

         return DefibrillatorMapper.map_records( data.fetchall() )

      finally:
         cur.close()
