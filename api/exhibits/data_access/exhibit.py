from __future__ import annotations

from .exhibit_mapper import map_region_exhibit_rows
from .region_exhibit_record import RegionExhibitRecord
from ...types import Connection


def fetch_exhibit_names( conn: Connection ) -> list[ str ]:
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


def fetch_exhibit_names_in_region( conn: Connection, region: str ) -> list[ str ]:
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


def fetch_region_exhibit_rows( conn: Connection ) -> list[ RegionExhibitRecord ]:
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

      return map_region_exhibit_rows( data.fetchall() )

   finally:
      cur.close()


def fetch_animal_names_in_exhibit( conn: Connection, exhibit: str ) -> list[ str ]:
   cur = conn.cursor()

   try:
      data = cur.execute(
         """   SELECT
                  a.SPECIES
               FROM Animal a
               JOIN Enclosure e
                  ON a.SPECIES = e.SPECIES
               WHERE e.EXHIBIT = ?;
         """, ( exhibit, ) )

      return [ row[ 0 ] for row in data.fetchall() ]

   finally:
      cur.close()
