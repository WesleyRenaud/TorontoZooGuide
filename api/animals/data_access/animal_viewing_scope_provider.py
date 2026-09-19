from __future__ import annotations

from ..domain.animal_viewing_scope import AnimalViewingScope
from ...types import Types


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
