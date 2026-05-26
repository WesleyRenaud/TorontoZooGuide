from __future__ import annotations

from ...shared.enums import AnimalViewingScope
from ...types import Connection


def fetch_animal_viewing_scopes(
      conn: Connection,
      species: str,
      exhibit: str ) -> list[ AnimalViewingScope ]:
   rows = conn.execute(
      """   SELECT DISTINCT LOWER( ENCLOSURE_TYPE ) AS VIEWING_SCOPE
            FROM EnclosureViewing
            WHERE SPECIES = ?
               AND EXHIBIT = ?
            ORDER BY VIEWING_SCOPE;
      """,
      (
         species,
         exhibit,
      ) ).fetchall()

   return [
      scope for scope in (
         AnimalViewingScope.normalize( row[ 'VIEWING_SCOPE' ] )
         for row in rows
      )
      if scope != None
   ]
