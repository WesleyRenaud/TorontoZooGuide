from __future__ import annotations

from ..domain.exhibit_season import ExhibitSeason
from ..domain.exhibit_species import ExhibitSpecies
from .exhibit_mapper import ExhibitMapper
from .exhibit_season_mapper import ExhibitSeasonMapper
from .exhibit_species_mapper import ExhibitSpeciesMapper
from .region_exhibit_record import RegionExhibitRecord
from ...shared.enums.position import Position
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

         return [ row[ Position.FIRST ] for row in data.fetchall() ]

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

         return [ row[ Position.FIRST ] for row in data.fetchall() ]

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
   def fetch_seasons( cls, conn: Types.Connection ) -> list[ ExhibitSeason ]:
      rows = conn.execute(
         """   SELECT
                  NAME,
                  OPEN_START_MONTH,
                  OPEN_END_MONTH
               FROM Exhibit;
         """ ).fetchall()

      return ExhibitSeasonMapper.map_records( rows )


   @classmethod
   def fetch_species_by_exhibit( cls, conn: Types.Connection ) -> list[ ExhibitSpecies ]:
      rows = conn.execute(
         """   SELECT
                  EXHIBIT,
                  SPECIES
               FROM Enclosure
               ORDER BY SPECIES;
         """ ).fetchall()

      return ExhibitSpeciesMapper.map_records( rows )


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

         return [ row[ Position.FIRST ] for row in data.fetchall() ]

      finally:
         cur.close()
