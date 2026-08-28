from __future__ import annotations

from ...models import Pavilion
from .pavilion_mapper import PavilionMapper
from ...types import Types


class PavilionProvider():
   @classmethod
   def fetch_pavilions( cls, conn: Types.Connection ) -> list[ Pavilion ]:
      cur = conn.cursor()

      try:
         data = cur.execute(
            """   SELECT
                     p.NAME,
                     p.REGION,
                     p.DESCRIPTION,
                     p.X_COORD,
                     p.Y_COORD
                  FROM Pavilion p;
            """ )

         return PavilionMapper.map_records( data.fetchall() )

      finally:
         cur.close()
