from __future__ import annotations

from ... import zoo
from ...types import Connection


def fetch_pavilions( conn: Connection ) -> list[ zoo.Pavilion ]:
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

      return [
         zoo.Pavilion(
            name=row[ 'NAME' ],
            region=row[ 'REGION' ],
            description=row[ 'DESCRIPTION' ],
            x_coord=row[ 'X_COORD' ],
            y_coord=row[ 'Y_COORD' ] )
         for row in data.fetchall()
      ]

   finally:
      cur.close()
