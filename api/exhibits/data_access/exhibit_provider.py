from __future__ import annotations

from .exhibit_mapper import ExhibitMapper
from .region_exhibit_record import RegionExhibitRecord
from ...types import Types


class ExhibitProvider():
   @classmethod
   def fetch_exhibit_names( cls, conn: Types.Connection ) -> list[ str ]:
      cur = conn.cursor()

      try:
         data = cur.execute(
            """   SELECT
                     e.NAME
                  FROM Exhibit e;
            """ )

         return [ row[ 0 ] for row in data.fetchall() ]

      finally:
         cur.close()


   @classmethod
   def fetch_exhibit_names_in_region( cls, conn: Types.Connection, region: str ) -> list[ str ]:
      cur = conn.cursor()

      try:
         data = cur.execute(
            """  SELECT
                    e.NAME
                 FROM Exhibit e
                 WHERE e.REGION = ?;
            """, ( region, ) )

         return [ row[ 0 ] for row in data.fetchall() ]

      finally:
         cur.close()


   @classmethod
   def fetch_region_exhibit_rows( cls, conn: Types.Connection ) -> list[ RegionExhibitRecord ]:
      cur = conn.cursor()

      try:
         data = cur.execute(
            """   SELECT
                     r.NAME AS REGION_NAME,
                     e.NAME AS EXHIBIT_NAME
                  FROM Region r
                  LEFT JOIN Exhibit e
                     ON e.REGION = r.NAME
                  ORDER BY r.NAME, e.NAME;
            """ )

         return ExhibitMapper.map_region_exhibit_rows( data.fetchall() )

      finally:
         cur.close()


   @classmethod
   def fetch_animal_names_in_exhibit( cls, conn: Types.Connection, exhibit: str ) -> list[ str ]:
      cur = conn.cursor()

      try:
         data = cur.execute(
            """   SELECT DISTINCT
                     a.SPECIES
                  FROM Animal a
                  JOIN Enclosure e
                     ON a.SPECIES = e.SPECIES
                  WHERE e.EXHIBIT = ?;
            """, ( exhibit, ) )

         return [ row[ 0 ] for row in data.fetchall() ]

      finally:
         cur.close()
