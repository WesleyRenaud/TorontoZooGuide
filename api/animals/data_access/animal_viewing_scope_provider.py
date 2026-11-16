from __future__ import annotations

from ..domain.animal_viewing_scope import AnimalViewingScope
from .enclosure_viewing_mapper import EnclosureViewingMapper
from ...types import Types
from ...walk_graph.domain.viewing_spot_reference import ViewingSpotReference


class AnimalViewingScopeProvider():
   @classmethod
   def fetch_animal_viewing_scopes(
         cls,
         conn: Types.Connection,
         species: str,
         exhibit: str ) -> list[ AnimalViewingScope ]:
      rows = conn.execute(
         """   SELECT NAME
               FROM EnclosureViewing
               WHERE SPECIES = ?
                  AND EXHIBIT = ?
               ORDER BY NAME;
         """,
         (
            species,
            exhibit,
         ) ).fetchall()

      return [
         AnimalViewingScope.from_enclosure_name( row[ 'NAME' ] )
         for row in rows
      ]


   @classmethod
   def fetch_animal_enclosures(
         cls,
         conn: Types.Connection ) -> list[ ViewingSpotReference ]:
      rows = conn.execute(
         """   SELECT SPECIES, EXHIBIT, NAME
               FROM EnclosureViewing
               WHERE NAME IS NOT NULL
                  AND NAME != ''
               ORDER BY SPECIES, EXHIBIT, NAME;
         """
      ).fetchall()
      return EnclosureViewingMapper.map_records( rows )

