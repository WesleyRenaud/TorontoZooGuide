from __future__ import annotations

from ..domain.animal_viewing_scope import AnimalViewingScope
from ...types import Types


class AnimalOffDisplayStatusResolver():
   @classmethod
   def delete_conflicting_animal_statuses(
         cls,
         cur: Types.Cursor,
         species: str,
         exhibit: str,
         viewing_scopes: list[ AnimalViewingScope ] ) -> None:
      viewing_scope_placeholders = ', '.join( '?' for _ in viewing_scopes )
      cur.execute(
         f"""   DELETE FROM AnimalStatus
               WHERE SPECIES = ?
                  AND EXHIBIT = ?
                  AND VIEWING_SCOPE IN ( { viewing_scope_placeholders } );
         """,
         (
            species,
            exhibit,
            *( viewing_scope.enclosure_name for viewing_scope in viewing_scopes ),
         ) )
